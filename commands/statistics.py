from .base_command import BaseCommand
import statistics

class StatisticsCommands(BaseCommand):
    """Basic statistical functions."""

    def get_commands(self):
        return {
            'mean': self.cmd_mean,
            'stdev': self.cmd_stdev,
        }

    def get_help(self):
        return {
            'mean': "MEAN: Compute mean. Usage: mean <comma-separated numbers>",
            'stdev': "STDEV: Compute standard deviation. Usage: stdev <comma-separated numbers>",
        }

    def _parse_numbers(self, argstr: str):
        tokens = [t.strip() for t in argstr.split(',') if t.strip()]
        nums = [float(self.parser.parse(t)) for t in tokens]
        return nums

    def cmd_mean(self, args: str):
        nums = self._parse_numbers(args)
        self.formatter.display_result(statistics.mean(nums), "Mean")

    def cmd_stdev(self, args: str):
        nums = self._parse_numbers(args)
        self.formatter.display_result(statistics.stdev(nums), "Std Dev")
