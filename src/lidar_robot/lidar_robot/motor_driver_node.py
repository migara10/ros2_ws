import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import serial
import time


class MotorDriverNode(Node):
    def __init__(self):
        super().__init__('motor_driver_node')

        self.declare_parameter('serial_port', '/dev/arduino')
        self.declare_parameter('baudrate', 115200)
        self.declare_parameter('wheel_separation', 0.05)
        self.declare_parameter('max_speed', 255)
        self.declare_parameter('max_linear_vel', 4.0)
        self.declare_parameter('min_pwm', 100)
        self.declare_parameter('left_trim', 1.0)
        self.declare_parameter('right_trim', 0.5)

        serial_port = self.get_parameter('serial_port').value
        baudrate = self.get_parameter('baudrate').value
        self.wheel_separation = self.get_parameter('wheel_separation').value
        self.max_speed = self.get_parameter('max_speed').value
        self.max_linear_vel = self.get_parameter('max_linear_vel').value
        self.min_pwm = self.get_parameter('min_pwm').value
        self.left_trim = self.get_parameter('left_trim').value
        self.right_trim = self.get_parameter('right_trim').value

        try:
            self.serial_conn = serial.Serial(serial_port, baudrate, timeout=1)
            time.sleep(2)
            self.get_logger().info(f'Connected to Arduino on {serial_port}')
        except serial.SerialException as e:
            self.get_logger().error(f'Failed to connect to Arduino: {e}')
            raise

        self.subscription = self.create_subscription(
            Twist, 'cmd_vel', self.cmd_vel_callback, 10
        )

        self.last_cmd_time = self.get_clock().now()
        self.timer = self.create_timer(0.1, self.safety_check)

        self.get_logger().info('Motor Driver Node started, listening to /cmd_vel')

    def cmd_vel_callback(self, msg: Twist):
        linear = msg.linear.x
        angular = msg.angular.z

        left_vel = linear - (angular * self.wheel_separation / 2.0)
        right_vel = linear + (angular * self.wheel_separation / 2.0)

        left_pwm = self.velocity_to_pwm(left_vel, self.left_trim)
        right_pwm = self.velocity_to_pwm(right_vel, self.right_trim)

        self.send_command(left_pwm, right_pwm)
        self.last_cmd_time = self.get_clock().now()

    def velocity_to_pwm(self, vel, trim):
        if abs(vel) < 0.001:
            return 0

        pwm = int((vel / self.max_linear_vel) * self.max_speed * trim)
        pwm = max(-self.max_speed, min(self.max_speed, pwm))

        if 0 < abs(pwm) < self.min_pwm:
            pwm = self.min_pwm if pwm > 0 else -self.min_pwm

        return pwm

    def send_command(self, left_pwm, right_pwm):
        command = f"L{left_pwm} R{right_pwm}\n"
        try:
            self.serial_conn.write(command.encode())
        except serial.SerialException as e:
            self.get_logger().error(f'Serial write failed: {e}')

    def safety_check(self):
        now = self.get_clock().now()
        elapsed = (now - self.last_cmd_time).nanoseconds / 1e9
        if elapsed > 0.3:
            self.send_command(0, 0)

    def destroy_node(self):
        self.send_command(0, 0)
        self.serial_conn.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = MotorDriverNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()