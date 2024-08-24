This is a small breakdown of what this code tries to achieve

1. There are two lanes defined here from which the cars will move straight ahead with **randomized rates** of appearing and wth **randomized speed**.

2. There is one traffice light for each lane ( They seem to change position whenever the color changes which IG is something I could try to fix). These lights change color in an **interval of 30 seconds**.

3. The cars stop whenever the light on their lane is red and accordingly for green. They disapear once they cross the screen length.

4. The Traffic lights to have a definite time duration before changing color there is a dynamic adaptation system that counts if the number of cars in any lane is **more than or equal to 10**; if so then the code will **bypass** the timer and open the lane with more traffic pressure.

5. When the bypass happens there is a text that appears on the screen to indicate that it was a **dynamic change**. Moreover, there is an **onscreen counter** that keeps track of how many cars are on each lane to better see the dynamic changes. 