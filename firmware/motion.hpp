// SPDX-License-Identifier: MIT
// AI-assisted independent implementation. No upstream firmware is copied.
#pragma once
#include <array>
#include <cstdint>
namespace actuator {
enum class State { Disarmed, Idle, Moving, LimitOpen, Stopped, Fault, Timeout, LinkLost };
struct Inputs { std::array<bool,4> allow{{false,false,false,false}}; bool driver_fault=true; };
struct Axis { State state=State::Disarmed; int direction=0; uint32_t start=0, timeout=0; };
class Controller {
 public:
  static constexpr uint32_t qualification_ms=20, heartbeat_ms=500, max_motion_ms=5000;
  std::array<Axis,2> axes{};
  void sample(uint32_t now,const Inputs& v) {
    bool changed=!seen_||v.allow!=in_.allow||v.driver_fault!=in_.driver_fault;
    if(changed) stable_since_=now;
    seen_=true; in_=v;
    if(v.driver_fault||(!v.allow[0]&&!v.allow[1])||(!v.allow[2]&&!v.allow[3])) { off(State::Fault); return; }
    if(armed_ && elapsed(now,last_heartbeat_)>=heartbeat_ms) {off(State::LinkLost);return;}
    for(unsigned i=0;i<2;i++) if(axes[i].state==State::Moving) {
      auto &a=axes[i];
      if(!v.allow[2*i+(a.direction>0?1:0)]) {a.state=State::LimitOpen;a.direction=0;}
      else if(elapsed(now,a.start)>=a.timeout) {a.state=State::Timeout;a.direction=0;armed_=false;for(auto &other:axes) if(other.state==State::Moving){other.state=State::Stopped;other.direction=0;}}
    }
  }
  bool arm(uint32_t now) {
    if(!seen_ || in_.driver_fault || elapsed(now,stable_since_)<qualification_ms ||
       (!in_.allow[0]&&!in_.allow[1])||(!in_.allow[2]&&!in_.allow[3])) return false;
    for(auto &a:axes) if(a.state==State::Moving)return false;
    armed_=true;last_heartbeat_=now;for(auto &a:axes)a={State::Idle,0,0,0};return true;
  }
  bool start(unsigned id,int direction,uint32_t duration,uint32_t now) {
    if(!armed_||id>=2||(direction!=1&&direction!=-1)||duration==0||duration>max_motion_ms||elapsed(now,last_heartbeat_)>=heartbeat_ms)return false;
    auto &a=axes[id];
    if(a.state==State::Moving||!in_.allow[2*id+(direction>0?1:0)])return false;
    a={State::Moving,direction,now,duration};return true;
  }
  void heartbeat(uint32_t now){if(armed_)last_heartbeat_=now;}
  void stop(){off(State::Stopped);}
  bool armed()const{return armed_;}
  int requested_direction(unsigned id)const{return armed_&&id<2&&axes[id].state==State::Moving?axes[id].direction:0;}
 private:
  Inputs in_{};bool armed_=false,seen_=false;uint32_t stable_since_=0,last_heartbeat_=0;
  static uint32_t elapsed(uint32_t n,uint32_t b){return n-b;}
  void off(State s){armed_=false;for(auto &a:axes){a.state=s;a.direction=0;}}
};
}
