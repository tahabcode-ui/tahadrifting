
import math
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Ellipse, Line, Triangle
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.metrics import dp


class DriftGame(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.elapsed = 0
        self.score = 0
        self.best = 0
        self.car_angle = 0
        self.mistake_time = 0
        self.started = False
        self.crashed = False
        self.drift_pressed = False

        self.bind(pos=self.draw, size=self.draw)
        Clock.schedule_interval(self.update, 1 / 60)

    def reset(self):
        self.elapsed = 0
        self.score = 0
        self.car_angle = 0
        self.mistake_time = 0
        self.started = False
        self.crashed = False
        self.drift_pressed = False
        self.draw()

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False

        if self.crashed:
            self.reset()
            return True

        if touch.y < self.y + self.height * 0.48:
            self.drift_pressed = True
            self.started = True
            return True

        return False

    def on_touch_up(self, touch):
        self.drift_pressed = False
        return True

    def update(self, dt):
        if not self.started or self.crashed:
            return

        dt = min(dt, 0.04)
        self.elapsed += dt

        curve = math.sin(self.elapsed * 1.15) * 0.58
        target = curve if self.drift_pressed else 0

        speed = 4.2 if self.drift_pressed else 2.7
        self.car_angle += (target - self.car_angle) * min(1, speed * dt)

        if self.drift_pressed:
            self.score += dt * (20 + abs(curve) * 12)

        error = abs(curve - self.car_angle)

        if abs(curve) > 0.30 and error > 0.48:
            self.mistake_time += dt
        else:
            self.mistake_time = max(
                0, self.mistake_time - dt * 1.5
            )

        if self.mistake_time > 0.9:
            self.crashed = True
            self.best = max(self.best, int(self.score))

        self.draw()

    def draw(self, *args):
        self.canvas.clear()

        w = self.width
        h = self.height

        if w <= 0 or h <= 0:
            return

        with self.canvas:
            # Background
            Color(0.025, 0.045, 0.085, 1)
            Rectangle(pos=self.pos, size=self.size)

            # Stars
            Color(0.45, 0.65, 0.85, 0.55)

            for i in range(35):
                sx = self.x + (i * 83 % max(1, int(w)))
                sy = self.y + (i * 137 % max(1, int(h)))
                Ellipse(
                    pos=(sx, sy),
                    size=(dp(1.5), dp(1.5))
                )

            # Road
            road_points = []

            for i in range(51):
                ratio = i / 50
                road_time = self.elapsed + (1 - ratio) * 3.7

                center = self.x + w * (
                    0.5 + math.sin(road_time * 1.15) * 0.13
                )

                yy = self.y + h * ratio
                half = w * 0.205

                road_points.append((center, yy, half))

            # Road surface
            Color(0.15, 0.19, 0.26, 1)

            for i in range(50):
                c1, y1, half1 = road_points[i]
                c2, y2, half2 = road_points[i + 1]

                l1 = c1 - half1
                r1 = c1 + half1
                l2 = c2 - half2
                r2 = c2 + half2

                Triangle(points=[
                    l1, y1, r1, y1, l2, y2
                ])

                Triangle(points=[
                    r1, y1, r2, y2, l2, y2
                ])

            # Road edges
            Color(0.45, 0.75, 0.95, 0.8)

            left = []
            right = []
            center_line = []

            for center, yy, half in road_points:
                left.extend([center - half, yy])
                right.extend([center + half, yy])
                center_line.extend([center, yy])

            Line(points=left, width=dp(3))
            Line(points=right, width=dp(3))

            # Dashed center line
            Color(0.95, 0.85, 0.55, 0.8)

            for i in range(0, 48, 5):
                start = i * 2

                Line(
                    points=center_line[start:start + 4],
                    width=dp(2)
                )

            # Car
            cx = self.x + w * (
                0.5 + math.sin(self.elapsed * 1.15) * 0.13
            )

            cy = self.y + h * 0.23

            car_length = w * 0.105
            car_width = w * 0.052
            a = self.car_angle

            def rotate(px, py):
                return (
                    cx + px * math.cos(a) - py * math.sin(a),
                    cy + px * math.sin(a) + py * math.cos(a)
                )

            p1 = rotate(-car_length / 2, -car_width / 2)
            p2 = rotate(car_length / 2, -car_width / 2)
            p3 = rotate(car_length / 2, car_width / 2)
            p4 = rotate(-car_length / 2, car_width / 2)

            # Car body
            Color(0.02, 0.72, 0.98, 1)

            Triangle(points=[
                p1[0], p1[1],
                p2[0], p2[1],
                p3[0], p3[1]
            ])

            Triangle(points=[
                p1[0], p1[1],
                p3[0], p3[1],
                p4[0], p4[1]
            ])

            # Car outline
            Color(0.75, 0.95, 1, 1)
            Line(points=[
                p1[0], p1[1],
                p2[0], p2[1],
                p3[0], p3[1],
                p4[0], p4[1],
                p1[0], p1[1]
            ], width=dp(1.5))

            # Car window
            q1 = rotate(-car_length * 0.03, -car_width * 0.32)
            q2 = rotate(car_length * 0.25, -car_width * 0.32)
            q3 = rotate(car_length * 0.25, car_width * 0.32)
            q4 = rotate(-car_length * 0.03, car_width * 0.32)

            Color(0.025, 0.10, 0.17, 1)
            Triangle(points=[
                q1[0], q1[1],
                q2[0], q2[1],
                q3[0], q3[1]
            ])
            Triangle(points=[
                q1[0], q1[1],
                q3[0], q3[1],
                q4[0], q4[1]
            ])


class TahaDriftApp(App):

    def build(self):
        self.title = "Taha Drift"

        root = FloatLayout()

        self.game = DriftGame()
        root.add_widget(self.game)

        self.title_label = Label(
            text="TAHA DRIFT",
            font_size="25sp",
            bold=True,
            color=(0.1, 0.8, 1, 1),
            size_hint=(None, None),
            size=(dp(280), dp(50)),
            pos_hint={"center_x": 0.5, "top": 0.98}
        )
        root.add_widget(self.title_label)

        self.score_label = Label(
            text="SCORE 0",
            font_size="23sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(dp(220), dp(45)),
            pos_hint={"center_x": 0.5, "top": 0.90}
        )
        root.add_widget(self.score_label)

        self.best_label = Label(
            text="BEST 0",
            font_size="14sp",
            color=(0.5, 0.8, 1, 1),
            size_hint=(None, None),
            size=(dp(150), dp(35)),
            pos_hint={"right": 0.98, "top": 0.84}
        )
        root.add_widget(self.best_label)

        self.hint_label = Label(
            text="HOLD LOWER SCREEN TO DRIFT",
            font_size="14sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(0.95, None),
            height=dp(45),
            pos_hint={"center_x": 0.5, "y": 0.25}
        )
        root.add_widget(self.hint_label)

        Clock.schedule_interval(self.refresh_ui, 0.1)

        return root

    def refresh_ui(self, dt):
        game = self.game

        self.score_label.text = f"SCORE {int(game.score)}"
        self.best_label.text = f"BEST {max(game.best, int(game.score))}"

        if game.crashed:
            self.hint_label.text = "CRASH! TAP LOWER SCREEN TO RETRY"

        elif game.started:
            self.hint_label.text = "RELEASE TO STRAIGHTEN"

        else:
            self.hint_label.text = "HOLD LOWER SCREEN TO DRIFT"


if __name__ == "__main__":
    TahaDriftApp().run()
