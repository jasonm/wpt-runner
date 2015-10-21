See work in `run.py` and `poller.py`.

Proposed core functionality:

1. Enqueue WPT runs (cron/heroku scheduler/etc)
2. Poll WPT for completion
3. Download and persist run data
4. Show charts

Similar work:

* Etsy's [wpt-script](https://github.com/etsy/wpt-script) is designed to work with your own private WPT infrastructure.  [Conference talk video demonstrating it](https://www.youtube.com/watch?v=RjHh6ULFHiM).
