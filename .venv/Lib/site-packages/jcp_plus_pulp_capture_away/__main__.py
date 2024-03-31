from aw_core.log import setup_logging

from jcp_plus_pulp_capture_away.afk import AFKWatcher
from jcp_plus_pulp_capture_away.config import parse_args


def main() -> None:
    args = parse_args()

    # Set up logging
    setup_logging(
        "jcp-plus-pulp-capture-away",
        testing=args.testing,
        verbose=args.verbose,
        log_stderr=True,
        log_file=True,
    )

    # Start watcher
    watcher = AFKWatcher(args, testing=args.testing)
    watcher.run()


if __name__ == "__main__":
    main()
