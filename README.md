#### SparklePop

<img src="https://github.com/danielbeach/sparklepop/blob/main/imgs/sparklepop.png" width="300">


SparklePop is a simple Python package designed to check the free disk space of an AWS RDS instance. It leverages AWS CloudWatch to retrieve the necessary metrics. This package is intended for users who need a straightforward way to monitor disk space without setting up complex alerts.

## Installation

To install SparklePop, you can use pip:

```bash
pip install sparklepop
```

## Usage

### Initialization

First, you need to create an instance of the `SparklePop` class. You need to provide the RDS instance identifier and optionally the AWS region (default is `us-east-1`). `boto3` is in use, so authenticate to AWS as you normally would via environment variables etc.

```python
from sparklepop import SparklePop

rds_instance = "your_rds_instance_identifier"
region = "us-east-1"

sparklepop = SparklePop(rds_instance, region)
```

### Get Free Disk Space

To get the free disk space in gigabytes:

```python
free_space = sparklepop.get_free_disk_space()
print(f"Free disk space: {free_space} GB")
```

### Check Free Disk Space

To check if the free disk space is below a certain threshold and raise an error if it is:
(the default threshold is 10GB, feel free to change it)

```python
sparklepop.check_on_free_disk_space(minimum_gb=10)
```

## Example

Here's a complete example:

```python
from sparklepop import SparklePop

# Initialize the SparklePop object
rds_instance = "your_rds_instance_identifier"
region = "us-east-1"
sparklepop = SparklePop(rds_instance, region)

# Get free disk space
free_space = sparklepop.get_free_disk_space()
print(f"Free disk space: {free_space} GB")

# Check if free disk space is above the threshold
sparklepop.check_on_free_disk_space(minimum_gb=10)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.