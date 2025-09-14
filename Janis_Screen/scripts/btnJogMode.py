if(d.getJogMode( ) == JogMode.Continous):
	gui.btnJogMode.setText( "Step" )
	d.setJogMode(JogMode.Step)
else:
	gui.btnJogMode.setText( "Continuous" )
	d.setJogMode(JogMode.Continous)
