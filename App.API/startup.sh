echo "starting on display ${DISPLAY}..."
xdpyinfo
if which x11vnc &>/dev/null; then
  ! pgrep -a x11vnc && x11vnc -bg -forever -nopw -quiet -display WAIT$DISPLAY &
fi
! pgrep -a Xvfb && Xvfb $DISPLAY -screen 0 1024x768x24 &
sleep 1
if which fluxbox &>/dev/null; then
  ! pgrep -a fluxbox && fluxbox 2>/dev/null &
fi
echo "IP: $(hostname -I) ($(hostname))"
echo "display setup complete"

uvicorn server:app --host 0.0.0.0 --port 8000