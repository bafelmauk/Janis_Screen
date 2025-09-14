if(d.getJogStep( ) == 1.000):
	d.setJogStep(0.100)
elif(d.getJogStep( ) == 0.100):
	d.setJogStep(0.010)
elif(d.getJogStep( ) == 0.010):
	d.setJogStep(0.001)
elif(d.getJogStep( ) == 0.001):
	d.setJogStep(1.000)
else:
	print("setting JOG step to 0.010")
	d.setJogStep("0.010")
