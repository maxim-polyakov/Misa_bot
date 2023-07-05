#!/bin/bash
  python nltkdownload.py&
  python telegram_main.py&
  python discord_main.py&
  wait