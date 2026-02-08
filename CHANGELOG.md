# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GPU warm-up scripts (`warm_up_gpu.py` and `warm_up_gpu.sh`) for performance optimization
- GPU quota check script (`request_gpu_quota.sh`)
- S3 bucket cleanup script (`cleanup_s3_buckets.sh`)
- VPC cleanup script with Batch resources support (`cleanup_vpcs.sh`)
- Cost alert setup scripts (Python and Bash versions)
- Comprehensive documentation in `docs/` directory
- GitHub Actions workflows for deployment and testing
- Detailed job monitoring with status updates
- `.gitattributes` for consistent line endings

### Changed
- Switched from Spot to On-Demand instances for reliability
- Improved `aws_submit_job.py` with detailed status monitoring
- Enhanced README with GPU quota requirements
- Reorganized documentation structure
- Updated deployment workflows with cleanup steps

### Fixed
- Terraform state management issues
- VPC limit exceeded errors
- Batch compute environment provisioning
- ECR repository conflicts
- IAM role and CloudWatch log group conflicts

### Security
- Added environment protection for test-deployment workflow
- Implemented authorization checks for workflow execution
- Created comprehensive security documentation

## [1.0.0] - 2026-02-07

### Added
- Initial release
- AI music generation with MusicGen
- AWS Bedrock integration for image generation
- Video composition pipeline
- AWS Batch deployment with GPU support
- Terraform infrastructure as code
- Docker containerization
- Multiple quality presets (quick, balanced, quality, experimental)
- Multiple resolution options (HD, FHD, 2K, 4K, YouTube)
- S3 output storage
- CloudWatch logging

