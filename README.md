Inspiration
As Computer Science students, we spend tons of time focused on our laptop screens, leading to incorrect posture habits that accumulate over time. Since many other participants in this hackathon are in the same situation as us, we were inspired to create software that can help reinforce correct posture when working on your laptop.

What it does
Posturite is a live camera detection app that scans your posture while at your computer, telling you what you need to fix. It helps users who are often challenger by bad posture while on their computers stay healthy while working for extended periods of time.

How we built it
We built posturite with OpenCV and MediaPipe. We used OpenCV to build our front end of the desktop app, and used MediaPipe for joint detection to build our algorithm for the posture detection and fixes.

Challenges we ran into
It was very tedious getting the project repo set up, and getting MediaPipe to recognize and detect our body parts.

Accomplishments that we're proud of
We are proud of successfully implementing an algorithm that detects how close a user is to the webcam to detect slouching

What we learned
Tkinter frontend framework
Implementing and utilizing computer vision
Basics of git
Collaborative software design
What's next for Posturite
We are hoping to make the frontend look prettier and smoother and add a feature/option for users that will help stricter reinforce their posture by disabling their keyboard whenever slouching is detected. To achieve this we need to first improve and optimize our detecting algorithm to be very stable in its detection to avoid disrupting with user's work.

