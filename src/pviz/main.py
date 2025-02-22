#!/usr/bin/env python3

import argparse
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Tuple
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box


class Period(Enum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"


@dataclass
class TimeUnit:
    minutes: float
    formatted: str


class AvailabilityCalculator:
    MINUTES_PER_PERIOD = {
        Period.DAY: 24 * 60,
        Period.WEEK: 7 * 24 * 60,
        Period.MONTH: 30 * 24 * 60,
        Period.QUARTER: 90 * 24 * 60,
        Period.YEAR: 365 * 24 * 60,
    }

    def __init__(self, availability_percentage: float):
        if not 0 <= availability_percentage <= 100:
            raise ValueError("Availability must be between 0 and 100")
        self.availability = availability_percentage / 100

    def calculate_downtime(self, period: Period) -> TimeUnit:
        total_minutes = self.MINUTES_PER_PERIOD[period]
        downtime_minutes = total_minutes * (1 - self.availability)
        return TimeUnit(
            minutes=downtime_minutes, formatted=self._format_duration(downtime_minutes)
        )

    def calculate_all_periods(self) -> Dict[Period, TimeUnit]:
        return {period: self.calculate_downtime(period) for period in Period}

    def compare_with(
        self, other_availability: float
    ) -> Dict[Period, Tuple[TimeUnit, TimeUnit]]:
        if self.availability == other_availability / 100:
            raise ValueError("Cannot compare identical availability values")
        other_calc = AvailabilityCalculator(other_availability)
        return {
            period: (
                self.calculate_downtime(period),
                other_calc.calculate_downtime(period),
            )
            for period in Period
        }

    @staticmethod
    def _format_duration(minutes: float) -> str:
        if minutes < 1:
            return f"{minutes * 60:.1f} seconds"

        hours = int(minutes // 60)
        remaining_minutes = minutes % 60

        if hours == 0:
            return f"{remaining_minutes:.1f} minutes"
        elif remaining_minutes == 0:
            return f"{hours} hours"
        else:
            return f"{hours} hours {remaining_minutes:.1f} minutes"


class AvailabilityVisualizer:
    def __init__(self):
        self.console = Console()

    def visualize_single(self, availability: float, focus_period: Optional[str] = None):
        calculator = AvailabilityCalculator(availability)

        title = f"[bold blue]Availability Impact Analysis: {availability}%[/bold blue]"
        self.console.print(Panel(title, box=box.DOUBLE))

        table = Table(box=box.SIMPLE_HEAVY)
        table.add_column("Time Period", style="cyan", justify="left")
        table.add_column("Maximum Downtime", style="yellow", justify="right")

        periods = [Period(focus_period)] if focus_period else list(Period)

        for period in periods:
            downtime = calculator.calculate_downtime(period)
            table.add_row(period.value.capitalize(), downtime.formatted)

        self.console.print(table)

    def visualize_comparison(self, availability1: float, availability2: float):
        calculator1 = AvailabilityCalculator(availability1)
        comparison = calculator1.compare_with(availability2)

        title = f"[bold blue]Availability Comparison: {availability1}% vs {availability2}%[/bold blue]"
        self.console.print(Panel(title, box=box.DOUBLE))

        # Calculate improvement percentage
        improvement = (
            ((100 - availability1) - (100 - availability2))
            / (100 - availability1)
            * 100
        )
        self.console.print(f"[yellow]Downtime reduction: {improvement:.1f}%[/yellow]\n")

        table = Table(box=box.SIMPLE_HEAVY)
        table.add_column("Time Period", style="cyan", justify="left")
        table.add_column(f"{availability1}%", style="yellow", justify="right")
        table.add_column(f"{availability2}%", style="yellow", justify="right")

        for period, (first, second) in comparison.items():
            table.add_row(period.value.capitalize(), first.formatted, second.formatted)

        self.console.print(table)


class CLI:
    def __init__(self):
        self.parser = self._create_parser()
        self.visualizer = AvailabilityVisualizer()

    def _create_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="Analyze service availability and allowed downtime",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s analyze 99.99
  %(prog)s analyze 99.99 --focus quarter
  %(prog)s compare 99.9 99.95
            """,
        )

        subparsers = parser.add_subparsers(dest="command", help="Commands")

        # Analyze command
        analyze_parser = subparsers.add_parser(
            "analyze", help="Analyze a single availability target"
        )
        analyze_parser.add_argument(
            "availability", type=float, help="Availability target (e.g., 99.9)"
        )
        analyze_parser.add_argument(
            "--focus",
            choices=[p.value for p in Period],
            help="Focus on a specific time period",
        )

        # Compare command
        compare_parser = subparsers.add_parser(
            "compare", help="Compare two availability targets"
        )
        compare_parser.add_argument(
            "availability1", type=float, help="First availability target (e.g., 99.9)"
        )
        compare_parser.add_argument(
            "availability2", type=float, help="Second availability target (e.g., 99.95)"
        )

        return parser

    def run(self, args: Optional[list] = None) -> int:
        try:
            parsed_args = self.parser.parse_args(args)

            if parsed_args.command is None:
                self.parser.print_help()
                return 1

            if parsed_args.command == "analyze":
                self.visualizer.visualize_single(
                    parsed_args.availability, parsed_args.focus
                )
            elif parsed_args.command == "compare":
                self.visualizer.visualize_comparison(
                    parsed_args.availability1, parsed_args.availability2
                )

            return 0

        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            return 1


def main():
    cli = CLI()
    sys.exit(cli.run())


if __name__ == "__main__":
    main()
