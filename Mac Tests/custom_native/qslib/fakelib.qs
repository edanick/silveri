QSLIB20.1.0


0.6.0
fakelib.sr‡mod export fakelib;import{fakeCompute}from fakebridge;string fakeStatus(int x){if(fakeCompute(x)==null){return "stub";}return "real";}