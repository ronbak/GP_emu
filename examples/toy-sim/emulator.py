import gp_emu as g

#### set up everything - config, emulator
conf = g.config("toy-sim_config")
emul = g.setup(conf)

#### repeat train and validate, then retrain into final emulator
g.training_loop(emul, conf, auto=True)
g.final_build(emul, conf, auto=True)

#### see full prediction, plot "mean" or "var"
g.plot(emul, [0],[1],[0.3], "mean")
g.plot(emul, [0,1],[2],[0.3], "mean")
