from jcp_plus_pulp_core.log import setup_logging

from jcp_plus_pulp_monitor_away.afk import AFKMonitor
from jcp_plus_pulp_monitor_away.config import parse_args


def main() -> None:
    args = parse_args()

    # Set up logging
    setup_logging(
        "jcp-plus-pulp-monitor-away",
        testing=args.testing,
        verbose=args.verbose,
        log_stderr=True,
        log_file=True,
    )

    # Start watcher
    watcher = AFKMonitor(args, testing=args.testing)
    watcher.run()


if __name__ == "__main__":
    main()
