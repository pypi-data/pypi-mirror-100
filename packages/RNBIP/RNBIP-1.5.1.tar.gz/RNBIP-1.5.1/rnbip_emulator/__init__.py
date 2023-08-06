import sys

# from assembler impo
from rnbip_emulator.rnbip_assembler import rnbip_assembler
from rnbip_emulator.emulator_backend import single_bus_emulator
from rnbip_emulator import emulator_gui

def main():
  inst_emulator  = single_bus_emulator()
  inst_assembler = rnbip_assembler()
  app = emulator_gui.QApplication(sys.argv)
  ex = emulator_gui.MainWidow(inst_emulator,inst_assembler)
  app.exec_()
  inst_emulator.end_emulation()
  print(len(inst_emulator.TraceVector))
  sys.exit()
  inst_emulator  = single_bus_emulator()
  inst_assembler = rnbip_assembler()
  app = emulator_gui.QApplication(sys.argv)
  ex = emulator_gui.MainWidow(inst_emulator,inst_assembler)
  app.exec_()
  inst_emulator.end_emulation()
  print(len(inst_emulator.TraceVector))
  sys.exit()