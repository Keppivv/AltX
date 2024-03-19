# Source code yet to be released

Instructions:
  Roblox game client name has to be "Roblox" (cAseSenSiTiVe)
  Left click system tray icon -> Settings -> AFK Check (Toggle, Indicated by native Windows notification)


-- -- -- --
Native Windows notification appears after 16 minutes of inactivity, automatically resets after that.
While "Roblox" window is focused, and mouse click acitvity is detected -> Reset timer
-- -- -- --

TODO:
  Config.ini for inactivity delay and Client name.
  New Client Detection with process.
  Move Client Name detection to Legacy/Failsafe (using pygetwindow).
  Add support for multi-instance AFK Detection.
  Add Optional Multi-instance Mutex creation. (Experimental, Byfron might see it as a third party modification)
