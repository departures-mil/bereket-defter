import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, "masaustu"))
