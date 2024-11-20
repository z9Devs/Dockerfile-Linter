from .core import parse_dockerfile
from .checks import check_base_image, check_non_root_user, check_optimized_run
from .report import generate_report

__version__ = "0.1.0"