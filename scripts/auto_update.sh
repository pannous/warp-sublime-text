#!/bin/zsh
# Daily (cron): regenerates the word lists from the warp main checkout, checks the package, and commits and pushes
# when the lists changed. A failure is loud: a macOS notification and a card on warp's to-do board (once per
# distinct failure, so a daily cron doesn't pile up cards).
#
# usage: scripts/auto_update.sh [path to warp checkout]

WARP=${1:-$HOME/dev/angles/warp}
PACKAGE=${0:A:h:h}
GENERATED=(Warp.sublime-syntax Warp.sublime-completions)
LAST_FAILURE=$HOME/.cache/sublime-words.last-failure
TODO=$HOME/dev/bin/todo

fail() {
	local reason=$1
	print -u2 "sublime-words FAILED: $reason"
	osascript -e "display notification \"${reason//\"/'}\" with title \"Warp Sublime words update failed\"" 2>/dev/null
	if [[ $(cat $LAST_FAILURE 2>/dev/null) != $reason ]]; then
		$TODO add "Sublime word lists (warp-sublime-text scripts/auto_update.sh) fail: $reason; log ~/.companion/logs/sublime-words.log" &&
			print -r -- $reason > $LAST_FAILURE
	fi
	exit 1
}

cd $PACKAGE || fail "no package folder $PACKAGE"
print "== $(date '+%F %T') sublime-words from $WARP @ $(git -C $WARP rev-parse --short HEAD)"
git pull --rebase --autostash -q || fail "git pull of the package failed"
words=$(python3 scripts/update_words.py $WARP 2>&1) || fail "update_words.py: ${${(f)words}[-1]}"
checks=$(python3 scripts/check_syntax.py 2>&1) || fail "check_syntax.py: $(print -r -- $checks | grep -m1 -iE 'fail|error')"
if git diff --quiet -- $GENERATED; then
	print "word lists unchanged"
else
	git diff --stat -- $GENERATED
	git commit -q -m "chore: word lists regenerated from warp $(git -C $WARP rev-parse --short HEAD)" -- $GENERATED &&
		git push -q || fail "commit or push of the regenerated word lists failed"
	print "word lists committed and pushed"
fi
rm -f $LAST_FAILURE
