#!/usr/bin/env python3

import config
import numpy as np
import subprocess
import os
from plot import plot_grid, plot_grid2, plot_ae

def echodo(cmd,file=None):
    subprocess.call(["echo"]+cmd)
    if file is None:
        subprocess.call(cmd)
    else:
        with open(file,"w") as f:
            subprocess.call(cmd,stdout=f)

def echo_out(cmd):
    subprocess.call(["echo"]+cmd)
    return subprocess.check_output(cmd)

class PlanException(BaseException):
    pass

options = {
    "lmcut" : "--search astar(lmcut())",
    "blind" : "--search astar(blind())",
    "hmax"  : "--search astar(hmax())",
    "mands" : "--search astar(merge_and_shrink(shrink_strategy=shrink_bisimulation(max_states=50000,greedy=false),merge_strategy=merge_dfp(),label_reduction=exact(before_shrinking=true,before_merging=false)))",
    "pdb"   : "--search astar(pdb())",
    "cpdb"  : "--search astar(cpdbs())",
    "ipdb"  : "--search astar(ipdb())",
    "zopdb"  : "--search astar(zopdbs())",
}

option = "blind"
sigma = 0.3
def latent_plan(init,goal,ae,mode = 'blind'):
    # temporary!
    if os.path.exists(ae.local("noise.csv")):
        raise PlanException("Don't run twice!")
    init = init.astype(float) + np.random.normal(0.0,sigma,init.shape)
    goal = goal.astype(float) + np.random.normal(0.0,sigma,goal.shape)
    init = init.clip(0,1)
    goal = goal.clip(0,1)
    ig_x, ig_z, ig_y, ig_b, ig_by = plot_ae(ae,np.array([init,goal]),"init_goal_noise.png")

    d = echo_out(["mktemp","-d"]).splitlines()[0].decode('utf-8')
    print(d)
    np.savetxt(d+"/noise.csv",ig_b.flatten().astype('int'),"%d")
    try:
        out = echo_out(["md5sum",d+"/noise.csv",ae.local("noise.csv")])
        tokens = out.split()
        if tokens[0] != tokens[2]:
            echodo(["cp",d+"/noise.csv",ae.local("noise.csv")])
    except subprocess.CalledProcessError:
        echodo(["cp",d+"/noise.csv",ae.local("noise.csv")])

    action_type = "all"
        
    # start planning
    plan_raw = ae.local("noise_{}.sasp.plan".format(action_type))
    plan     = ae.local("noise-{}-{}.plan".format(action_type,mode))
    echodo(["rm",plan])
    echodo(["make","-C","lisp","-j","1"])
    echodo(["make","-C",ae.path,"-f","../Makefile",
            # dummy pddl (text file with length 0)
            "domain.pddl",
            "noise_{}.sasp".format(action_type)])
    echodo(["planner-scripts/limit.sh","-v","-t","3600",
            "-o",options[mode],
            "--","fd-sas-clean",
            ae.local("noise_{}.sasp".format(action_type))])
    if not os.path.exists(plan_raw):
        raise PlanException("no plan found")
    echodo(["mv",plan_raw,plan])
    out = echo_out(["lisp/parse-plan.bin",plan,
                    *list(ig_b[0].flatten().astype('int').astype('str'))])
    lines = out.splitlines()
    if len(lines) is 2:
        raise PlanException("not an interesting problem")
    numbers = np.array([ [ int(s) for s in l.split() ] for l in lines ])
    print(numbers)
    plan_images = ae.decode_binary(numbers)
    plot_grid(plan_images,path=ae.local('{}-{}-noise.png'.format(action_type,mode)))
    plot_grid(plan_images.round(),path=ae.local('{}-{}-rounded-noise.png'.format(action_type,mode)))

from model import default_networks

def select(data,num):
    return data[np.random.randint(0,data.shape[0],num)]

def run_puzzle(path, network, p):
    from model import GumbelAE
    ae = default_networks[network](path)
    configs = np.array(list(p.generate_configs(9)))
    def convert(panels):
        return np.array([
            [i for i,x in enumerate(panels) if x == p]
            for p in range(9)]).reshape(-1)
    ig_c = [convert([8,0,6,5,4,7,2,3,1]),
            convert([0,1,2,3,4,5,6,7,8])]
    ig = p.states(3,3,ig_c)
    try:
        latent_plan(*ig, ae, option)
    except PlanException as e:
        print(e)

def run_lightsout(path, network, p):
    from model import GumbelAE
    ae = default_networks[network](path)
    configs = np.array(list(p.generate_configs(4)))
    ig_c = [[0,1,0,0,
             0,1,0,0,
             0,0,1,1,
             1,0,0,0,],
            np.zeros(16)]
    ig = p.states(4,ig_c)
    try:
        latent_plan(*ig, ae, option)
    except PlanException as e:
        print(e)

def run_hanoi10(path, network, p):
    from model import GumbelAE
    ae = default_networks[network](path)
    configs = np.array(list(p.generate_configs(10)))
    ig_c = [[0,0,0,0,0,0,0,0,0,0],
            [2,2,2,2,2,2,2,2,2,2]]
    ig = p.states(10,ig_c)
    try:
        latent_plan(*ig, ae, option)
    except PlanException as e:
        print(e)

def run_hanoi4(path, network, p):
    from model import GumbelAE
    ae = default_networks[network](path)
    configs = np.array(list(p.generate_configs(4)))
    ig_c = [[0,0,0,0],
            [2,2,2,2]]
    ig = p.states(4,ig_c)
    try:
        latent_plan(*ig, ae, option)
    except PlanException as e:
        print(e)


if __name__ == '__main__':
    import sys
    from importlib import import_module
    sys.argv.pop(0)
    option = sys.argv.pop(0)
    sigma = sys.argv.pop(0)
    eval(sys.argv[0])
    echodo(["samples/sync.sh"])
    
