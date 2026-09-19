// SPDX-License-Identifier: MIT
// Bench dry-run firmware: bridge RESET and PWM outputs NEVER enabled.
#include <cstdio>
#include "pico/stdlib.h"
#include "hardware/watchdog.h"
#include "motion.hpp"
#if defined(ENABLE_REAL_DRIVE) && ENABLE_REAL_DRIVE
#error "R0 has no validated power-stage driver. Real drive is intentionally blocked."
#endif
int main(){
 const unsigned outputs[]={12,9,11,13,8,10};
 for(auto pin:outputs){gpio_init(pin);gpio_put(pin,0);gpio_set_dir(pin,GPIO_OUT);}
 const unsigned limits[]={16,17,18,19};
 for(auto pin:limits){gpio_init(pin);gpio_set_dir(pin,GPIO_IN);gpio_disable_pulls(pin);gpio_set_input_hysteresis_enabled(pin,true);}
 gpio_init(14);gpio_set_dir(14,GPIO_IN);gpio_disable_pulls(14);
 stdio_init_all();watchdog_enable(100,true);actuator::Controller c;uint32_t last=0;
 while(true){
   uint32_t now=to_ms_since_boot(get_absolute_time());
   actuator::Inputs in;for(unsigned i=0;i<4;i++)in.allow[i]=gpio_get(limits[i]);in.driver_fault=!gpio_get(14);c.sample(now,in);
   int cmd=getchar_timeout_us(0);
   if(cmd=='a')printf("arm=%d\n",c.arm(now));
   else if(cmd=='h')c.heartbeat(now);
   else if(cmd=='s')c.stop();
   else if(cmd=='1')printf("request A+ accepted=%d\n",c.start(0,1,2000,now));
   else if(cmd=='2')printf("request A- accepted=%d\n",c.start(0,-1,2000,now));
   else if(cmd=='3')printf("request B+ accepted=%d\n",c.start(1,1,2000,now));
   else if(cmd=='4')printf("request B- accepted=%d\n",c.start(1,-1,2000,now));
   for(auto pin:outputs)gpio_put(pin,0);
   if(now-last>=200){last=now;printf("DRY_RUN allow=%d%d%d%d requested=%d,%d physical_drive=OFF\n",in.allow[0],in.allow[1],in.allow[2],in.allow[3],c.requested_direction(0),c.requested_direction(1));}
   watchdog_update();sleep_ms(1);
 }
}
