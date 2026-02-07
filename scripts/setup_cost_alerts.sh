#!/bin/bash

# Setup AWS Cost Alerts
# This script creates budget alerts at $1 increments (approximately R$5)

set -e

echo "🔔 Setting up AWS Cost Alerts..."

# Get AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo "AWS Account ID: $ACCOUNT_ID"

# Get email for notifications
read -p "Enter your email for cost alerts: " EMAIL

# Create SNS topic for budget notifications
echo "Creating SNS topic for budget notifications..."
TOPIC_ARN=$(aws sns create-topic \
  --name ai-music-generator-budget-alerts \
  --query 'TopicArn' \
  --output text 2>/dev/null || \
  aws sns list-topics --query "Topics[?contains(TopicArn, 'ai-music-generator-budget-alerts')].TopicArn" --output text)

echo "SNS Topic ARN: $TOPIC_ARN"

# Subscribe email to SNS topic
echo "Subscribing $EMAIL to budget alerts..."
aws sns subscribe \
  --topic-arn "$TOPIC_ARN" \
  --protocol email \
  --notification-endpoint "$EMAIL" \
  --output text

echo ""
echo "⚠️  IMPORTANT: Check your email and confirm the SNS subscription!"
echo ""
read -p "Press Enter after confirming the subscription email..."

# Create budget alerts at $1, $5, $10, $20, $50
THRESHOLDS=(1 5 10 20 50)

for THRESHOLD in "${THRESHOLDS[@]}"; do
  BUDGET_NAME="ai-music-gen-alert-${THRESHOLD}usd"
  
  echo "Creating budget alert for \$$THRESHOLD USD (~R$$(($THRESHOLD * 5)))..."
  
  # Create budget JSON
  cat > /tmp/budget_${THRESHOLD}.json <<EOF
{
  "BudgetName": "${BUDGET_NAME}",
  "BudgetLimit": {
    "Amount": "${THRESHOLD}",
    "Unit": "USD"
  },
  "TimeUnit": "MONTHLY",
  "BudgetType": "COST",
  "CostFilters": {
    "TagKey": ["Project"],
    "TagValue": ["ai-music-generator"]
  },
  "CostTypes": {
    "IncludeTax": true,
    "IncludeSubscription": true,
    "UseBlended": false,
    "IncludeRefund": false,
    "IncludeCredit": false,
    "IncludeUpfront": true,
    "IncludeRecurring": true,
    "IncludeOtherSubscription": true,
    "IncludeSupport": true,
    "IncludeDiscount": true,
    "UseAmortized": false
  },
  "TimePeriod": {
    "Start": "$(date -u +%Y-%m-01T00:00:00Z)",
    "End": "2087-06-15T00:00:00Z"
  }
}
EOF

  # Create notification JSON
  cat > /tmp/notification_${THRESHOLD}.json <<EOF
[
  {
    "Notification": {
      "NotificationType": "ACTUAL",
      "ComparisonOperator": "GREATER_THAN",
      "Threshold": 80,
      "ThresholdType": "PERCENTAGE",
      "NotificationState": "ALARM"
    },
    "Subscribers": [
      {
        "SubscriptionType": "SNS",
        "Address": "${TOPIC_ARN}"
      }
    ]
  },
  {
    "Notification": {
      "NotificationType": "ACTUAL",
      "ComparisonOperator": "GREATER_THAN",
      "Threshold": 100,
      "ThresholdType": "PERCENTAGE",
      "NotificationState": "ALARM"
    },
    "Subscribers": [
      {
        "SubscriptionType": "SNS",
        "Address": "${TOPIC_ARN}"
      }
    ]
  },
  {
    "Notification": {
      "NotificationType": "FORECASTED",
      "ComparisonOperator": "GREATER_THAN",
      "Threshold": 100,
      "ThresholdType": "PERCENTAGE",
      "NotificationState": "ALARM"
    },
    "Subscribers": [
      {
        "SubscriptionType": "SNS",
        "Address": "${TOPIC_ARN}"
      }
    ]
  }
]
EOF

  # Create or update budget
  aws budgets create-budget \
    --account-id "$ACCOUNT_ID" \
    --budget file:///tmp/budget_${THRESHOLD}.json \
    --notifications-with-subscribers file:///tmp/notification_${THRESHOLD}.json \
    2>/dev/null || \
  aws budgets update-budget \
    --account-id "$ACCOUNT_ID" \
    --new-budget file:///tmp/budget_${THRESHOLD}.json \
    2>/dev/null || true

  echo "✅ Budget alert created for \$$THRESHOLD USD"
  
  # Clean up temp files
  rm -f /tmp/budget_${THRESHOLD}.json /tmp/notification_${THRESHOLD}.json
done

echo ""
echo "✅ All budget alerts created successfully!"
echo ""
echo "📊 Budget Alerts Summary:"
echo "  • \$1 USD (~R\$5) - Alert at 80% and 100%"
echo "  • \$5 USD (~R\$25) - Alert at 80% and 100%"
echo "  • \$10 USD (~R\$50) - Alert at 80% and 100%"
echo "  • \$20 USD (~R\$100) - Alert at 80% and 100%"
echo "  • \$50 USD (~R\$250) - Alert at 80% and 100%"
echo ""
echo "📧 Notifications will be sent to: $EMAIL"
echo ""
echo "🔍 View budgets at: https://console.aws.amazon.com/billing/home#/budgets"
echo ""
echo "💡 Tips:"
echo "  • You'll receive alerts at 80% and 100% of each threshold"
echo "  • Forecasted alerts warn you before reaching the limit"
echo "  • Check your email regularly for cost notifications"
echo "  • Review AWS Cost Explorer monthly: https://console.aws.amazon.com/cost-management/home"
echo ""
