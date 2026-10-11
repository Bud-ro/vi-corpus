# MQTT-Connection-LocalQueue
A completely local queue-based implementation of the MQTT Connection class

This package is an example for how to create a new specific connection package based on the abstract Connection class.
The local queue implementation can be used for integration testing when a network connection is not available and when network functionality os not the goal of the test.
It can also be used to provide inter-process communication in a way where the connection is injectable at runtime, thus making it possible to change the course of communication through a message-abstarction layer with little pain.
