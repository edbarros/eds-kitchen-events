# Events agent playbook

Goal: keep `events.json` current for Ed's Kitchen (small-batch macadamia nut butter, Ovilla TX 76059) and alert Ed only when a genuinely good event appears.

## Each run
1. Read `events.json` from github.com/edbarros/eds-kitchen-events (main).
2. Research the DFW area (about 90 miles of Ovilla; flag anything over 75 miles as "worth the trip only if great"): holiday/craft/farmers markets, vendor calls, festivals, fall/winter 2026-27. Use the organizers' own pages for dates, fees, application links and the cottage-food rule. Search for new events AND changes to existing ones (dates, fees, deadline, closed/open status).
3. Update only what you can support from a source. Never invent fees, crowd sizes or dates. Use `st: "check"` and say what is unconfirmed in `nt`. Do not remove events; mark them `st: "closed"`. Keep ids stable. Dates are `MM-DD`, `ap` must be an https link.
4. Score every new or changed event 0-100 and store it in `rk` (higher = better):
   - Cottage food allowed (`ck: "yes"`) is required for a good event. `no` or unknown caps the score at 40.
   - Low competition (few other nut-butter or food-jar vendors, juried or capped vendor lists): up to 25 points.
   - Paid admission or premium crowd (ticketed, 5,000+ attendees, holiday-gift buyers, upscale area): up to 25 points.
   - Drive (`mi`): 25 points at 25 miles or less, down to 0 at 90 miles.
   - Open application with a deadline still ahead: up to 15 points.
   A "good event" is a score of 75+ that is new or newly open, with cottage food allowed.
5. Set `updated` to the current UTC time, run `python3 validate.py` (must print 0 bad), commit "events: <summary>" and push to main. If nothing changed, do not commit.
6. For each good event send ONE alert (never repeat an alert for the same id; keep alerted ids in `alerted.json` in the repo):
   - Title: `Good event: <name>` / Body: city, dates, fee, drive miles, deadline, apply link.
   - Primary: email to `iqib5ws0a6w1@ntfy.sh` (ntfy turns it into a phone push; subject = title, body = details) through the Gmail connector.
   - Also email kitchen@edersonbarros.com a short digest (new, changed, good events).
7. If you cannot push (GitHub not linked or push refused), do not lose the work: email the digest and the full proposed JSON for the changed events to kitchen@edersonbarros.com and say that the push failed.

Ed's devices pick up the change on the next app launch or Refresh. New events show a "NEW" tag.
