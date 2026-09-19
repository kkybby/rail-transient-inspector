#include "../firmware/motion.hpp"
#include <cassert>
#include <iostream>
using namespace actuator;
int main(){unsigned checks=0; auto ok=[&](bool v){assert(v);++checks;};
 Inputs good{{true,true,true,true},false}; Controller c;
 ok(!c.armed());ok(c.requested_direction(0)==0);ok(!c.arm(0));ok(!c.start(0,1,100,0));
 c.sample(0,good);ok(!c.arm(19));ok(c.arm(20));ok(!c.start(2,1,100,20));ok(!c.start(0,0,100,20));ok(!c.start(0,1,0,20));ok(!c.start(0,1,5001,20));
 ok(c.start(0,1,300,20));ok(c.requested_direction(0)==1);ok(!c.start(0,-1,300,21));
 auto v=good;v.allow[1]=false;c.sample(22,v);ok(c.axes[0].state==State::LimitOpen);ok(c.requested_direction(0)==0);ok(!c.start(0,1,300,23));
 ok(c.start(0,-1,300,23));ok(c.requested_direction(0)==-1);c.sample(24,v);ok(c.requested_direction(0)==-1);c.stop();ok(!c.armed());ok(c.requested_direction(0)==0);
 c.sample(25,good);ok(!c.arm(30));ok(c.arm(45));ok(c.start(1,-1,100,45));c.sample(145,good);ok(c.axes[1].state==State::Timeout);ok(!c.armed());ok(c.requested_direction(1)==0);
 ok(c.arm(146));ok(c.start(0,1,1000,146));ok(c.start(1,1,1000,146));c.sample(646,good);ok(c.axes[0].state==State::LinkLost);ok(c.requested_direction(1)==0);
 ok(c.arm(647));ok(c.start(0,1,1000,647));c.heartbeat(1000);c.sample(1100,good);ok(c.requested_direction(0)==1);
 v=good;v.driver_fault=true;c.sample(1101,v);ok(c.axes[0].state==State::Fault);ok(!c.arm(2000));c.sample(2100,good);ok(c.arm(2120));
 v=good;v.allow[0]=v.allow[1]=false;c.sample(2121,v);ok(!c.armed());ok(!c.arm(3000));
 c.sample(3100,good);ok(c.arm(3120));ok(c.start(0,1,100,3120));v=good;v.allow[1]=false;c.sample(3121,v);c.sample(3122,good);ok(c.requested_direction(0)==0);ok(c.axes[0].state==State::LimitOpen);
 Controller w;w.sample(0xfffffff0,good);ok(w.arm(4));ok(w.start(0,1,50,4));w.sample(54,good);ok(w.axes[0].state==State::Timeout);
 std::cout<<checks<<" state-machine assertions passed; host logic only, no motor tests.\n";
}
