#!/usr/bin/env python3
"""
Setup AWS Cost Alerts
Creates budget alerts at $1 increments (approximately R$5 each)
"""

import boto3
import sys
from datetime import datetime, timezone
from botocore.exceptions import ClientError

# Budget thresholds in USD (approximately R$5 each)
THRESHOLDS = [1, 5, 10, 20, 50]


def get_account_id():
    """Get AWS account ID"""
    sts = boto3.client("sts")
    return sts.get_caller_identity()["Account"]


def create_sns_topic():
    """Create SNS topic for budget notifications"""
    sns = boto3.client("sns")
    topic_name = "ai-music-generator-budget-alerts"

    try:
        # Try to create topic
        response = sns.create_topic(Name=topic_name)
        topic_arn = response["TopicArn"]
        print(f"✅ SNS Topic created: {topic_arn}")
    except ClientError as e:
        # Topic might already exist, get it
        topics = sns.list_topics()
        topic_arn = None
        for topic in topics["Topics"]:
            if topic_name in topic["TopicArn"]:
                topic_arn = topic["TopicArn"]
                print(f"✅ Using existing SNS Topic: {topic_arn}")
                break

        if not topic_arn:
            raise e

    return topic_arn


def subscribe_email(topic_arn, email):
    """Subscribe email to SNS topic"""
    sns = boto3.client("sns")

    try:
        sns.subscribe(TopicArn=topic_arn, Protocol="email", Endpoint=email)
        print(f"✅ Email subscription created: {email}")
        print("⚠️  IMPORTANT: Check your email and confirm the subscription!")
        return True
    except ClientError as e:
        print(f"❌ Error subscribing email: {e}")
        return False


def create_budget(account_id, topic_arn, threshold):
    """Create budget alert for given threshold"""
    budgets = boto3.client("budgets")
    budget_name = f"ai-music-gen-alert-{threshold}usd"

    # Budget configuration
    budget = {
        "BudgetName": budget_name,
        "BudgetLimit": {"Amount": str(threshold), "Unit": "USD"},
        "TimeUnit": "MONTHLY",
        "BudgetType": "COST",
        "CostTypes": {
            "IncludeTax": True,
            "IncludeSubscription": True,
            "UseBlended": False,
            "IncludeRefund": False,
            "IncludeCredit": False,
            "IncludeUpfront": True,
            "IncludeRecurring": True,
            "IncludeOtherSubscription": True,
            "IncludeSupport": True,
            "IncludeDiscount": True,
            "UseAmortized": False,
        },
        "TimePeriod": {
            "Start": datetime(datetime.now().year, datetime.now().month, 1, tzinfo=timezone.utc),
            "End": datetime(2087, 6, 15, tzinfo=timezone.utc),
        },
    }

    # Notifications configuration
    notifications = [
        {
            "Notification": {
                "NotificationType": "ACTUAL",
                "ComparisonOperator": "GREATER_THAN",
                "Threshold": 80,
                "ThresholdType": "PERCENTAGE",
                "NotificationState": "ALARM",
            },
            "Subscribers": [{"SubscriptionType": "SNS", "Address": topic_arn}],
        },
        {
            "Notification": {
                "NotificationType": "ACTUAL",
                "ComparisonOperator": "GREATER_THAN",
                "Threshold": 100,
                "ThresholdType": "PERCENTAGE",
                "NotificationState": "ALARM",
            },
            "Subscribers": [{"SubscriptionType": "SNS", "Address": topic_arn}],
        },
        {
            "Notification": {
                "NotificationType": "FORECASTED",
                "ComparisonOperator": "GREATER_THAN",
                "Threshold": 100,
                "ThresholdType": "PERCENTAGE",
                "NotificationState": "ALARM",
            },
            "Subscribers": [{"SubscriptionType": "SNS", "Address": topic_arn}],
        },
    ]

    try:
        # Try to create budget
        budgets.create_budget(AccountId=account_id, Budget=budget, NotificationsWithSubscribers=notifications)
        print(f"✅ Budget alert created for ${threshold} USD (~R${threshold * 5})")
    except ClientError as e:
        if "DuplicateRecordException" in str(e):
            # Budget already exists, update it
            try:
                budgets.update_budget(AccountId=account_id, NewBudget=budget)
                print(f"✅ Budget alert updated for ${threshold} USD (~R${threshold * 5})")
            except ClientError as update_error:
                print(f"⚠️  Warning: Could not update budget for ${threshold}: {update_error}")
        else:
            print(f"❌ Error creating budget for ${threshold}: {e}")


def main():
    print("🔔 Setting up AWS Cost Alerts...")
    print()

    # Get AWS account ID
    try:
        account_id = get_account_id()
        print(f"AWS Account ID: {account_id}")
        print()
    except Exception as e:
        print(f"❌ Error getting AWS account ID: {e}")
        print("Make sure you have AWS credentials configured (aws configure)")
        sys.exit(1)

    # Get email for notifications
    email = input("Enter your email for cost alerts: ").strip()
    if not email or "@" not in email:
        print("❌ Invalid email address")
        sys.exit(1)

    print()

    # Create SNS topic
    try:
        topic_arn = create_sns_topic()
    except Exception as e:
        print(f"❌ Error creating SNS topic: {e}")
        sys.exit(1)

    print()

    # Subscribe email
    if not subscribe_email(topic_arn, email):
        print("⚠️  Warning: Email subscription failed, but continuing...")

    print()
    input("Press Enter after confirming the subscription email...")
    print()

    # Create budget alerts
    print("Creating budget alerts...")
    for threshold in THRESHOLDS:
        create_budget(account_id, topic_arn, threshold)

    print()
    print("=" * 70)
    print("✅ All budget alerts created successfully!")
    print("=" * 70)
    print()
    print("📊 Budget Alerts Summary:")
    print("  • $1 USD (~R$5) - Alert at 80% and 100%")
    print("  • $5 USD (~R$25) - Alert at 80% and 100%")
    print("  • $10 USD (~R$50) - Alert at 80% and 100%")
    print("  • $20 USD (~R$100) - Alert at 80% and 100%")
    print("  • $50 USD (~R$250) - Alert at 80% and 100%")
    print()
    print(f"📧 Notifications will be sent to: {email}")
    print()
    print("🔍 View budgets at: https://console.aws.amazon.com/billing/home#/budgets")
    print()
    print("💡 Tips:")
    print("  • You'll receive alerts at 80% and 100% of each threshold")
    print("  • Forecasted alerts warn you before reaching the limit")
    print("  • Check your email regularly for cost notifications")
    print("  • Review AWS Cost Explorer monthly:")
    print("    https://console.aws.amazon.com/cost-management/home")
    print()


if __name__ == "__main__":
    main()
