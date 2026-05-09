# Adaptive Traction Control System for Autonomous Mobile Robots

## Project Overview
This repository contains an autonomous navigation system designed to solve the **Velocity-Friction Mismatch** problem in mobile robotics. Standard "Open-Loop" controllers fail when a robot transitions between disparate surfaces (e.g., from smooth tile to high-friction carpet), leading to navigational drift and odometry errors.

This system utilizes a **Dual-Loop Adaptive Controller** that combines **Computer Vision** (surface classification) and **Odometry Feedback** (real-time speed correction) to maintain a constant target velocity regardless of environmental resistance.

---

## The Problem: Physics vs. Programming
In robotics, "Dumb" or Open-Loop control assumes that a specific power output always results in a specific speed. In real-world environments:
* **Surface Transitions:** Moving onto carpet can result in a **60-70% reduction in actual speed** despite a constant motor command.
* **Odometry Drift:** If a robot relies on time-based distance calculation, speed loss results in the robot becoming "lost" in its internal map.
* **Asymmetric Friction:** Uneven terrain causes differential drag, leading to heading (yaw) instability and veering.

---

## The Solution: Dual-Loop Adaptation
The "Smart" controller implemented in this project operates on two distinct feedback layers:

### 1. Perception Layer (Vision)
Using a downward-facing camera sensor, the system calculates the average pixel intensity of the ground plane.
* **High Intensity (>150):** Classified as **TILE**.
* **Low Intensity (<100):** Classified as **CARPET**.

By identifying the surface *before* the robot is fully submerged in the friction change, the system can pre-emptively prepare for torque adjustment.

### 2. Correction Layer (Feedback)
The system monitors the `Actual_Velocity` from the Gazebo Odometry topic.
* **Error Calculation:** $e = v_{target} - v_{actual}$
* **Adaptive Push:** When the surface is identified as CARPET and a speed drop is detected, the system applies an **Adaptive Torque Multiplier** to compensate for the friction loss.
* **Stability Control:** The system monitors the Yaw (orientation) and applies a Proportional counter-steer to ensure the robot maintains a straight heading.

---

## Comparative Performance Results

| Metric | Open-Loop ("Dumb") | Adaptive ("Smart") |
| :--- | :--- | :--- |
| **Target Speed** | 0.25 m/s | 0.25 m/s |
| **Speed on Tile** | 0.249 m/s | 0.250 m/s |
| **Speed on Carpet** | 0.082 m/s | 0.248 m/s |
| **Max Heading Error** | 1.1° | 0.1° |
| **Adaptive Effort** | 0.00% | +15.00% |

### Log Verification
In testing, the **Open-Loop** system demonstrated significant velocity decay upon terrain transition. The **Adaptive** system utilized high-frequency telemetry to ramp up `ADAPT_PWR` in response to camera intensity drops, shielding the robot's velocity from environmental friction.

---

## Technical Constraints
Performance was verified via **High-Frequency Telemetry Logs**. This approach ensured the simulation maintained a **Real-Time Factor (RTF)** of >0.9 on the testing hardware, providing high-fidelity data for the control loop without the overhead of screen-recording software.

## License
MIT License
