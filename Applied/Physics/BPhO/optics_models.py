import pygame
import numpy as np

# Configuration constants
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
FRAMERATE = 30
MARGIN = 50
IMAGE_SCALE_FACTOR = 8
BLACK = (40, 40, 40)
FOCAL_LENGTH = 250
CONCAVE_MIRROR_RADIUS = 300


# =============================================================================
# PHYSICS UTILITIES
# =============================================================================


class PhysicsUtils:
    """Mathematical utility functions for physics calculations."""

    @staticmethod
    def calculate_ray_intersection(point1, direction1, point2, direction2):
        """Calculate where two rays intersect."""
        x1, y1 = point1
        dx1, dy1 = direction1
        x2, y2 = point2
        dx2, dy2 = direction2

        denominator = dx1 * dy2 - dy1 * dx2
        if abs(denominator) < 0.001:
            return None

        t1 = ((x2 - x1) * dy2 - (y2 - y1) * dx2) / denominator
        intersection_x = x1 + t1 * dx1
        intersection_y = y1 + t1 * dy1

        return (intersection_x, intersection_y)

    @staticmethod
    def calculate_circle_intersection_horizontal(center_x, center_y, radius, pixel_y):
        """Calculate where a horizontal ray hits a circle."""
        dy = pixel_y - center_y
        discriminant = radius * radius - dy * dy

        if discriminant < 0:
            return None

        dx = discriminant**0.5
        x1 = center_x - dx
        x2 = center_x + dx

        return (x1, pixel_y), (x2, pixel_y)

    @staticmethod
    def calculate_circle_ray_intersection(
        center_x, center_y, radius, pixel_x, pixel_y, target_x, target_y
    ):
        """Calculate where a ray from one point towards another hits a circle."""
        dx_ray = target_x - pixel_x
        dy_ray = target_y - pixel_y

        if abs(dx_ray) < 0.001 and abs(dy_ray) < 0.001:
            return None

        a = dx_ray * dx_ray + dy_ray * dy_ray
        b = 2 * ((pixel_x - center_x) * dx_ray + (pixel_y - center_y) * dy_ray)
        c = (pixel_x - center_x) ** 2 + (pixel_y - center_y) ** 2 - radius**2

        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return None

        t1 = (-b - discriminant**0.5) / (2 * a)
        t2 = (-b + discriminant**0.5) / (2 * a)

        return t1, t2

    @staticmethod
    def calculate_reflected_ray(hit_point, center_x, center_y, incident_direction):
        """Calculate the reflected ray direction given hit point and incident direction."""
        hit_x, hit_y = hit_point
        incident_x, incident_y = incident_direction

        normal_x = hit_x - center_x
        normal_y = hit_y - center_y
        normal_length = (normal_x * normal_x + normal_y * normal_y) ** 0.5

        if normal_length > 0:
            normal_x /= normal_length
            normal_y /= normal_length

        dot_product = incident_x * normal_x + incident_y * normal_y
        reflected_x = incident_x - 2 * dot_product * normal_x
        reflected_y = incident_y - 2 * dot_product * normal_y

        return (reflected_x, reflected_y)

    @staticmethod
    def calculate_screen_intersection(
        start_x, start_y, dx, dy, screen_width, screen_height
    ):
        """Calculate where a ray intersects the screen boundaries."""
        if abs(dx) < 0.001 and abs(dy) < 0.001:
            return (start_x, start_y)

        t_values = []

        if dx > 0:
            t_values.append((screen_width - start_x) / dx)
        elif dx < 0:
            t_values.append(-start_x / dx)

        if dy > 0:
            t_values.append((screen_height - start_y) / dy)
        elif dy < 0:
            t_values.append(-start_y / dy)

        valid_t = [t for t in t_values if t > 0]
        if valid_t:
            t = min(valid_t)
            end_x = start_x + t * dx
            end_y = start_y + t * dy
            return (int(end_x), int(end_y))

        return (start_x, start_y)


class RayDrawer:
    """Utility class for drawing rays and dashed lines."""

    @staticmethod
    def draw_dashed_line(
        screen, start_point, end_point, color, thickness, dash_length=8, gap_length=4
    ):
        """Draw a dashed line between two points."""
        start_x, start_y = start_point
        end_x, end_y = end_point

        total_dx = end_x - start_x
        total_dy = end_y - start_y
        total_distance = (total_dx * total_dx + total_dy * total_dy) ** 0.5

        if total_distance < 0.1:
            return

        unit_dx = total_dx / total_distance
        unit_dy = total_dy / total_distance

        current_distance = 0
        while current_distance < total_distance:
            dash_start_x = start_x + current_distance * unit_dx
            dash_start_y = start_y + current_distance * unit_dy

            dash_end_distance = min(current_distance + dash_length, total_distance)
            dash_end_x = start_x + dash_end_distance * unit_dx
            dash_end_y = start_y + dash_end_distance * unit_dy

            pygame.draw.line(
                screen,
                color,
                (int(dash_start_x), int(dash_start_y)),
                (int(dash_end_x), int(dash_end_y)),
                thickness,
            )

            current_distance += dash_length + gap_length

    @staticmethod
    def calculate_screen_edge_intersection(
        start_x, start_y, direction_x, direction_y, screen_width, screen_height
    ):
        """Calculate where a ray hits the screen edge."""
        if direction_x == 0 and direction_y == 0:
            return None

        length = (direction_x**2 + direction_y**2) ** 0.5
        direction_x /= length
        direction_y /= length

        t_vals = []

        if direction_x > 0:
            t_vals.append((screen_width - start_x) / direction_x)
        elif direction_x < 0:
            t_vals.append(-start_x / direction_x)

        if direction_y > 0:
            t_vals.append((screen_height - start_y) / direction_y)
        elif direction_y < 0:
            t_vals.append(-start_y / direction_y)

        valid_t_vals = [t for t in t_vals if t > 0]
        if valid_t_vals:
            t = min(valid_t_vals)
            edge_x = start_x + direction_x * t
            edge_y = start_y + direction_y * t
            return (int(edge_x), int(edge_y))
        return None


# =============================================================================
# BASE OPTICAL ELEMENT CLASS
# =============================================================================


class OpticalElement:
    """Base class for all optical elements."""

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.physics = PhysicsUtils()
        self.ray_drawer = RayDrawer()

    def transform(self, world_x, world_y):
        """Transform coordinates - to be implemented by subclasses."""
        raise NotImplementedError

    def pixel_transformation(
        self, surface, image_center_pos, screen_width=None, screen_height=None
    ):
        """Apply transformation to surface - to be implemented by subclasses."""
        raise NotImplementedError

    def get_position(self, original_center, screen_width=None, screen_height=None):
        """Calculate transformed position - to be implemented by subclasses."""
        raise NotImplementedError

    def draw_reference_lines(self, screen, screen_width=None, screen_height=None):
        """Draw reference lines - to be implemented by subclasses."""
        raise NotImplementedError

    def draw_guide_rays(
        self, screen, image_rect, screen_width=None, screen_height=None
    ):
        """Draw guide rays - to be implemented by subclasses."""
        pass

    def _get_pixel_position(self, image_rect):
        """Get the center topmost pixel position for guide rays."""
        image_center_x, image_center_y = image_rect.center
        image_width, image_height = image_rect.size
        return image_center_x, image_center_y - image_height // 2


# =============================================================================
# PLANE MIRROR CLASS
# =============================================================================


class PlaneMirror(OpticalElement):
    """Plane mirror transformation class."""

    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        self.mirror_line_x = screen_width // 2

    def transform(self, world_x, world_y):
        """Plane mirror: reflect (x,y) across the vertical mirror line."""
        distance_to_mirror = world_x - self.mirror_line_x
        reflected_x = self.mirror_line_x - distance_to_mirror
        return reflected_x, world_y

    def pixel_transformation(
        self, surface, image_center_pos, screen_width=None, screen_height=None
    ):
        """Apply plane mirror transformation using optimised inverse mapping."""
        width, height = surface.get_size()
        source_array = pygame.surfarray.array3d(surface)
        transformed_array = np.zeros_like(source_array)

        image_center_x, image_center_y = image_center_pos
        half_width, half_height = width // 2, height // 2
        transformed_center = self.get_position(image_center_pos)
        trans_center_x, trans_center_y = transformed_center

        for trans_x in range(width):
            for trans_y in range(height):
                trans_screen_x = trans_x - half_width + trans_center_x
                trans_screen_y = trans_y - half_height + trans_center_y

                orig_screen_x = 2 * self.mirror_line_x - trans_screen_x
                orig_screen_y = trans_screen_y

                orig_x = orig_screen_x - image_center_x + half_width
                orig_y = orig_screen_y - image_center_y + half_height

                if 0 <= orig_x < width and 0 <= orig_y < height:
                    transformed_array[trans_x, trans_y] = source_array[
                        int(orig_x), int(orig_y)
                    ]

        return pygame.surfarray.make_surface(transformed_array)

    def get_position(self, original_center, screen_width=None, screen_height=None):
        """Calculate the centre position of a plane mirror transformed image."""
        orig_x, orig_y = original_center
        transformed_x = 2 * self.mirror_line_x - orig_x
        transformed_y = orig_y

        transformed_x = max(MARGIN, min(self.screen_width - MARGIN, transformed_x))
        transformed_y = max(MARGIN, min(self.screen_height - MARGIN, transformed_y))

        return transformed_x, transformed_y

    def draw_reference_lines(self, screen, screen_width=None, screen_height=None):
        """Draw reference lines for plane mirror transformation."""
        pygame.draw.line(
            screen,
            (100, 100, 100),
            (self.mirror_line_x, 0),
            (self.mirror_line_x, self.screen_height),
            2,
        )

    def draw_guide_rays(
        self, screen, image_rect, screen_width=None, screen_height=None
    ):
        """Draw guide rays for the center topmost pixel of the original image."""
        pixel_x, pixel_y = self._get_pixel_position(image_rect)

        ray_colour = (255, 0, 0)
        extension_colour = (255, 100, 100)
        intersection_colour = (255, 100, 100)
        ray_thickness = 2
        circle_radius = 4

        # Ray 1: Horizontal ray from pixel to mirror
        horizontal_hit_x = self.mirror_line_x
        horizontal_hit_y = pixel_y
        horizontal_hit = (horizontal_hit_x, horizontal_hit_y)

        # Ray 2: Ray from pixel through center of screen to mirror
        screen_center_x = self.screen_width // 2
        screen_center_y = self.screen_height // 2

        dx = screen_center_x - pixel_x
        dy = screen_center_y - pixel_y

        if abs(dx) < 0.001:
            center_hit_x = self.mirror_line_x
            center_hit_y = pixel_y
        else:
            t = (self.mirror_line_x - pixel_x) / dx
            center_hit_x = self.mirror_line_x
            center_hit_y = pixel_y + t * dy

        center_hit = (center_hit_x, center_hit_y)

        # Draw incident rays
        pygame.draw.line(
            screen, ray_colour, (pixel_x, pixel_y), horizontal_hit, ray_thickness
        )
        pygame.draw.line(
            screen, ray_colour, (pixel_x, pixel_y), center_hit, ray_thickness
        )

        # Calculate reflected rays
        horizontal_reflected_direction = (1, 0)
        horizontal_end = self.physics.calculate_screen_intersection(
            horizontal_hit_x,
            horizontal_hit_y,
            horizontal_reflected_direction[0],
            horizontal_reflected_direction[1],
            self.screen_width,
            self.screen_height,
        )

        incident_dx = center_hit_x - pixel_x
        incident_dy = center_hit_y - pixel_y
        incident_length = (incident_dx * incident_dx + incident_dy * incident_dy) ** 0.5
        if incident_length > 0:
            incident_dx /= incident_length
            incident_dy /= incident_length

        center_reflected_direction = (-incident_dx, incident_dy)
        center_end = self.physics.calculate_screen_intersection(
            center_hit_x,
            center_hit_y,
            center_reflected_direction[0],
            center_reflected_direction[1],
            self.screen_width,
            self.screen_height,
        )

        # Draw reflected rays
        if horizontal_end:
            pygame.draw.line(
                screen, ray_colour, horizontal_hit, horizontal_end, ray_thickness
            )
        else:
            pygame.draw.line(
                screen,
                ray_colour,
                horizontal_hit,
                (self.screen_width, horizontal_hit_y),
                ray_thickness,
            )

        if center_end:
            pygame.draw.line(screen, ray_colour, center_hit, center_end, ray_thickness)

        # Calculate and draw virtual image
        distance_to_mirror = pixel_x - self.mirror_line_x
        virtual_image_x = self.mirror_line_x - distance_to_mirror
        virtual_image_y = pixel_y
        virtual_image_pos = (virtual_image_x, virtual_image_y)

        if (
            0 <= virtual_image_x < self.screen_width
            and 0 <= virtual_image_y < self.screen_height
        ):
            self.ray_drawer.draw_dashed_line(
                screen,
                horizontal_hit,
                virtual_image_pos,
                extension_colour,
                ray_thickness,
            )
            self.ray_drawer.draw_dashed_line(
                screen, center_hit, virtual_image_pos, extension_colour, ray_thickness
            )
            pygame.draw.circle(
                screen,
                intersection_colour,
                (int(virtual_image_x), int(virtual_image_y)),
                circle_radius,
            )

        pygame.draw.circle(
            screen, ray_colour, (int(pixel_x), int(pixel_y)), circle_radius
        )


# =============================================================================
# MIRROR BASE CLASS
# =============================================================================


class SphericalMirror(OpticalElement):
    """Base class for spherical mirrors (concave and convex)."""

    def __init__(self, screen_width, screen_height, is_concave=True):
        super().__init__(screen_width, screen_height)
        self.mirror_radius = CONCAVE_MIRROR_RADIUS
        self.mirror_center_x = self.mirror_radius + 200
        self.mirror_center_y = screen_height // 2
        self.is_concave = is_concave

    def pixel_transformation(
        self, surface, image_center_pos, screen_width=None, screen_height=None
    ):
        """Apply spherical mirror transformation with pixel stretching."""
        width, height = surface.get_size()
        source_array = pygame.surfarray.array3d(surface)

        transformed_surface = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA
        )
        transformed_surface.fill((0, 0, 0, 0))

        image_center_x, image_center_y = image_center_pos
        half_width = width // 2

        for orig_x in range(width):
            for orig_y in range(height):
                orig_screen_x = orig_x - half_width + image_center_x
                orig_screen_y = orig_y - height // 2 + image_center_y

                transformed_x, transformed_y = self.transform(
                    orig_screen_x, orig_screen_y
                )

                if (
                    0 <= transformed_x < self.screen_width
                    and 0 <= transformed_y < self.screen_height
                ):
                    dx = transformed_x - self.mirror_center_x
                    dy = transformed_y - self.mirror_center_y
                    distance_from_center = (dx * dx + dy * dy) ** 0.5

                    # Check if within mirror boundary and on correct side
                    mirror_side_condition = (
                        transformed_x <= self.mirror_center_x
                        if self.is_concave
                        else transformed_x >= self.mirror_center_x
                    )

                    if (
                        distance_from_center <= self.mirror_radius
                        and mirror_side_condition
                    ):
                        pixel_colour = source_array[orig_x, orig_y]
                        stretch_size = self._calculate_stretch_size(
                            distance_from_center
                        )
                        self._apply_pixel_stretching(
                            transformed_surface,
                            transformed_x,
                            transformed_y,
                            pixel_colour,
                            stretch_size,
                        )

        return transformed_surface

    def _calculate_stretch_size(self, distance_to_arc):
        """Calculate pixel stretch size based on distance to mirror arc."""
        distance_to_arc = abs(distance_to_arc - self.mirror_radius)

        if distance_to_arc < 30:
            return 4
        elif distance_to_arc < 60:
            return 4
        elif distance_to_arc < 100:
            return 3
        elif distance_to_arc < 140:
            return 3
        elif distance_to_arc < 180:
            return 2
        elif distance_to_arc < 220:
            return 2
        else:
            return 1

    def _apply_pixel_stretching(
        self, surface, center_x, center_y, pixel_colour, stretch_size
    ):
        """Apply pixel stretching around a center point."""
        center_x, center_y = int(center_x), int(center_y)
        half_stretch = stretch_size // 2

        for dx in range(-half_stretch, half_stretch + 1):
            for dy in range(-half_stretch, half_stretch + 1):
                pixel_x, pixel_y = center_x + dx, center_y + dy
                if (
                    0 <= pixel_x < self.screen_width
                    and 0 <= pixel_y < self.screen_height
                ):
                    px_dx = pixel_x - self.mirror_center_x
                    px_dy = pixel_y - self.mirror_center_y
                    px_distance = (px_dx * px_dx + px_dy * px_dy) ** 0.5

                    mirror_side_condition = (
                        pixel_x <= self.mirror_center_x
                        if self.is_concave
                        else pixel_x >= self.mirror_center_x
                    )

                    if px_distance <= self.mirror_radius and mirror_side_condition:
                        surface.set_at((pixel_x, pixel_y), pixel_colour)

    def get_position(self, original_center, screen_width=None, screen_height=None):
        """Calculate the centre position of a spherical mirror transformed image."""
        orig_x, orig_y = original_center
        transformed_x, transformed_y = self.transform(orig_x, orig_y)

        transformed_x = max(MARGIN, min(self.screen_width - MARGIN, transformed_x))
        transformed_y = max(MARGIN, min(self.screen_height - MARGIN, transformed_y))

        return transformed_x, transformed_y

    def draw_reference_lines(self, screen, screen_width=None, screen_height=None):
        """Draw spherical mirror shape and focal line."""
        mirror_colour = (150, 150, 150)

        # Draw semicircle
        for angle in range(-90, 91, 2):
            rad = np.radians(angle)
            x_offset = -self.mirror_radius if self.is_concave else self.mirror_radius
            x = self.mirror_center_x + x_offset * np.cos(rad)
            y = self.mirror_center_y + self.mirror_radius * np.sin(rad)

            if 0 <= x < self.screen_width and 0 <= y < self.screen_height:
                pygame.draw.circle(screen, mirror_colour, (int(x), int(y)), 2)

        # Draw focal line
        focal_colour = (100, 150, 100)
        pygame.draw.line(
            screen,
            focal_colour,
            (self.mirror_center_x, 0),
            (self.mirror_center_x, self.screen_height),
            2,
        )

        # Add focal point label
        font = pygame.font.Font(None, 24)
        f_text = font.render("F", True, focal_colour)
        screen.blit(f_text, (self.mirror_center_x + 5, self.mirror_center_y))

    def _calculate_mirror_intersection_horizontal(self, pixel_x, pixel_y):
        """Calculate where horizontal ray hits the mirror surface."""
        intersections = self.physics.calculate_circle_intersection_horizontal(
            self.mirror_center_x, self.mirror_center_y, self.mirror_radius, pixel_y
        )

        if intersections:
            left_intersection, right_intersection = intersections
            # Return appropriate intersection based on mirror type
            intersection = left_intersection if self.is_concave else right_intersection
            return (int(intersection[0]), int(pixel_y))
        return None

    def _calculate_mirror_intersection_focal(self, pixel_x, pixel_y):
        """Calculate where ray through focal point hits the mirror surface."""
        t_values = self.physics.calculate_circle_ray_intersection(
            self.mirror_center_x,
            self.mirror_center_y,
            self.mirror_radius,
            pixel_x,
            pixel_y,
            self.mirror_center_x,
            self.mirror_center_y,
        )

        if t_values:
            t1, t2 = t_values
            dx_ray = self.mirror_center_x - pixel_x
            dy_ray = self.mirror_center_y - pixel_y

            for t in [t1, t2]:
                if t > 0:
                    hit_x = pixel_x + t * dx_ray
                    hit_y = pixel_y + t * dy_ray
                    # Check correct side based on mirror type
                    side_condition = (
                        hit_x <= self.mirror_center_x
                        if self.is_concave
                        else hit_x >= self.mirror_center_x
                    )
                    if side_condition:
                        return (int(hit_x), int(hit_y))
        return None

    def _calculate_reflected_ray_direction(self, hit_point, incident_or_flag=None):
        """
        Calculate reflected direction given a hit point and either:
        - an explicit incident direction (tuple), or
        - a boolean flag (True => horizontal ray).
        Backwards-compatible: if second arg is bool, behave like previous is_horizontal flag.
        """
        hit_x, hit_y = hit_point

        # Compute surface normal (outward for concave, inward for convex as before)
        if self.is_concave:
            normal_x = hit_x - self.mirror_center_x
            normal_y = hit_y - self.mirror_center_y
        else:
            normal_x = self.mirror_center_x - hit_x
            normal_y = self.mirror_center_y - hit_y

        normal_len = (normal_x * normal_x + normal_y * normal_y) ** 0.5
        if normal_len > 0:
            normal_x /= normal_len
            normal_y /= normal_len

        # Interpret second argument: if it's a bool -> it's the old is_horizontal flag.
        incident_direction = None
        is_horizontal = False
        if isinstance(incident_or_flag, bool):
            is_horizontal = incident_or_flag
        elif isinstance(incident_or_flag, (tuple, list)):
            incident_direction = (float(incident_or_flag[0]), float(incident_or_flag[1]))

        # If no explicit incident direction provided, fall back to previous conventions.
        if incident_direction is None:
            if is_horizontal:
                # Parallel ray toward mirror: side depends on mirror type
                if self.is_concave:
                    incident_x, incident_y = -1.0, 0.0
                else:
                    incident_x, incident_y = 1.0, 0.0
            else:
                # fallback: vector toward mirror center (old behavior)
                incident_x = self.mirror_center_x - hit_x
                incident_y = self.mirror_center_y - hit_y
                inc_len = (incident_x * incident_x + incident_y * incident_y) ** 0.5
                if inc_len > 0:
                    incident_x /= inc_len
                    incident_y /= inc_len
        else:
            incident_x, incident_y = incident_direction
            inc_len = (incident_x * incident_x + incident_y * incident_y) ** 0.5
            if inc_len > 0:
                incident_x /= inc_len
                incident_y /= inc_len

        # Reflection: R = I - 2(I·N)N
        dot = incident_x * normal_x + incident_y * normal_y
        reflected_x = incident_x - 2 * dot * normal_x
        reflected_y = incident_y - 2 * dot * normal_y

        return (reflected_x, reflected_y)

    def _calculate_reflected_end(self, hit_point, reflected_direction):
        """Calculate where reflected ray ends (mirror boundary or screen edge)."""
        hit_x, hit_y = hit_point
        dx, dy = reflected_direction

        if abs(dx) < 0.001 and abs(dy) < 0.001:
            return hit_point

        # Convex mirror: skip mirror-boundary intersection check — go straight to screen edge
        if not self.is_concave:
            return self.ray_drawer.calculate_screen_edge_intersection(
                hit_x, hit_y, dx, dy, self.screen_width, self.screen_height
            )

        # For concave mirrors, check possible re-intersection with mirror
        a = dx * dx + dy * dy
        b = 2 * ((hit_x - self.mirror_center_x) * dx + (hit_y - self.mirror_center_y) * dy)
        c = ((hit_x - self.mirror_center_x) ** 2 +
            (hit_y - self.mirror_center_y) ** 2 - self.mirror_radius**2)

        discriminant = b * b - 4 * a * c
        mirror_intersection = None

        if discriminant >= 0:
            t1 = (-b + discriminant**0.5) / (2 * a)
            t2 = (-b - discriminant**0.5) / (2 * a)

            for t in [t1, t2]:
                if t > 0.001:
                    intersect_x = hit_x + t * dx
                    intersect_y = hit_y + t * dy
                    if intersect_x <= self.mirror_center_x:  # concave side
                        mirror_intersection = (int(intersect_x), int(intersect_y))
                        break

        # Calculate screen intersection
        screen_intersection = self.ray_drawer.calculate_screen_edge_intersection(
            hit_x, hit_y, dx, dy, self.screen_width, self.screen_height
        )

        # Return closer intersection
        if mirror_intersection and screen_intersection:
            mirror_dist_sq = (mirror_intersection[0] - hit_x) ** 2 + (mirror_intersection[1] - hit_y) ** 2
            screen_dist_sq = (screen_intersection[0] - hit_x) ** 2 + (screen_intersection[1] - hit_y) ** 2
            return mirror_intersection if mirror_dist_sq <= screen_dist_sq else screen_intersection
        elif mirror_intersection:
            return mirror_intersection
        elif screen_intersection:
            return screen_intersection
        else:
            return hit_point


# =============================================================================
# CONCAVE MIRROR CLASS
# =============================================================================


class ConcaveMirror(SphericalMirror):
    """Concave mirror transformation class."""

    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height, is_concave=True)

    def transform(self, world_x, world_y):
        """Concave mirror: Apply reflection using the given equations."""
        x_rel = world_x - self.mirror_center_x
        y_rel = world_y - self.mirror_center_y

        if abs(x_rel) < 2.0 or abs(y_rel) < 0.1:
            return world_x, world_y

        try:
            if self.mirror_radius * self.mirror_radius - y_rel * y_rel < 0:
                return world_x, world_y

            C = (self.mirror_radius * self.mirror_radius - y_rel * y_rel) ** 0.5
            theta = np.arctan(y_rel / C) if C > 0.1 else 0
            m = np.tan(2 * theta)

            denominator = y_rel / x_rel + m if abs(x_rel) > 0.1 else m
            if abs(denominator) < 0.001:
                return world_x, world_y

            X_rel = -(m * C - y_rel) / denominator
            Y_rel = (y_rel / x_rel) * X_rel if abs(x_rel) > 0.1 else 0

            return X_rel + self.mirror_center_x, Y_rel + self.mirror_center_y

        except (ZeroDivisionError, OverflowError, ValueError):
            return world_x, world_y

    def draw_guide_rays(self, screen, image_rect, screen_width=None, screen_height=None):
        """Draw guide rays for the center topmost pixel of the original image."""
        pixel_x, pixel_y = self._get_pixel_position(image_rect)
        
        ray_colour = (255, 0, 0)
        intersection_color = (255, 0, 0)
        ray_thickness = 2
        circle_radius = 4

        horizontal_hit = self._calculate_mirror_intersection_horizontal(pixel_x, pixel_y)
        focal_hit = self._calculate_mirror_intersection_focal(pixel_x, pixel_y)

        if horizontal_hit and focal_hit:
            # Draw incident rays (from object pixel to mirror hits)
            pygame.draw.line(screen, ray_colour, (pixel_x, pixel_y), horizontal_hit, ray_thickness)
            pygame.draw.line(screen, ray_colour, (pixel_x, pixel_y), focal_hit, ray_thickness)

            # Build actual incident direction vectors (normalized)
            def _normalize(vx, vy):
                l = (vx * vx + vy * vy) ** 0.5
                return (vx / l, vy / l) if l > 0 else (0.0, 0.0)

            h_inc = _normalize(horizontal_hit[0] - pixel_x, horizontal_hit[1] - pixel_y)
            f_inc = _normalize(focal_hit[0] - pixel_x, focal_hit[1] - pixel_y)

            # Calculate reflected directions using actual incident vectors
            horizontal_reflected = self._calculate_reflected_ray_direction(horizontal_hit, h_inc)
            focal_reflected = self._calculate_reflected_ray_direction(focal_hit, f_inc)

            # Find intersection of reflected rays (real image)
            intersection = self.physics.calculate_ray_intersection(
                horizontal_hit, horizontal_reflected, focal_hit, focal_reflected
            )

            if intersection:
                ix, iy = intersection
                dx = ix - self.mirror_center_x
                dy = iy - self.mirror_center_y
                distance_from_center = (dx * dx + dy * dy) ** 0.5
                within_mirror = (distance_from_center <= self.mirror_radius and ix <= self.mirror_center_x)

                if within_mirror:
                    pygame.draw.line(screen, ray_colour, horizontal_hit, intersection, ray_thickness)
                    pygame.draw.line(screen, ray_colour, focal_hit, intersection, ray_thickness)
                    pygame.draw.circle(screen, intersection_color, (int(ix), int(iy)), circle_radius)
                else:
                    horizontal_end = self._calculate_reflected_end(horizontal_hit, horizontal_reflected)
                    if horizontal_end:
                        pygame.draw.line(screen, ray_colour, horizontal_hit, horizontal_end, ray_thickness)

            else:
                # If no intersection, at least draw the reflected horizontal ray to edge
                horizontal_end = self._calculate_reflected_end(horizontal_hit, horizontal_reflected)
                if horizontal_end:
                    pygame.draw.line(screen, ray_colour, horizontal_hit, horizontal_end, ray_thickness)

            pygame.draw.circle(screen, ray_colour, (int(pixel_x), int(pixel_y)), circle_radius)


# =============================================================================
# CONVEX MIRROR CLASS
# =============================================================================


class ConvexMirror(SphericalMirror):
    """Convex mirror transformation class."""

    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height, is_concave=False)

    def transform(self, world_x, world_y):
        """Convex mirror: Apply reflection using the given equations."""
        x_rel = world_x - self.mirror_center_x
        y_rel = world_y - self.mirror_center_y

        if abs(x_rel) < 2.0 or abs(y_rel) < 0.1:
            return world_x, world_y

        try:
            if abs(x_rel) > 0.1:
                alpha = 0.5 * np.arctan(y_rel / x_rel)
            else:
                return world_x, world_y

            cos_2alpha = np.cos(2 * alpha)
            if abs(cos_2alpha) < 0.001:
                return world_x, world_y

            k = x_rel / cos_2alpha
            sin_alpha = np.sin(alpha)
            cos_alpha = np.cos(alpha)

            if abs(y_rel) < 0.1:
                return world_x, world_y

            denominator = (
                k / self.mirror_radius - cos_alpha + (x_rel / y_rel) * sin_alpha
            )
            if abs(denominator) < 0.001:
                return world_x, world_y

            Y_rel = k * sin_alpha / denominator
            X_rel = x_rel * Y_rel / y_rel if abs(y_rel) > 0.1 else 0

            return X_rel + self.mirror_center_x, Y_rel + self.mirror_center_y

        except (ZeroDivisionError, OverflowError, ValueError):
            return world_x, world_y

    def pixel_transformation(
        self, surface, image_center_pos, screen_width=None, screen_height=None
    ):
        """Apply convex mirror transformation without pixel stretching."""
        width, height = surface.get_size()
        source_array = pygame.surfarray.array3d(surface)

        transformed_surface = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA
        )
        transformed_surface.fill((0, 0, 0, 0))

        image_center_x, image_center_y = image_center_pos
        half_width = width // 2

        for orig_x in range(width):
            for orig_y in range(height):
                orig_screen_x = orig_x - half_width + image_center_x
                orig_screen_y = orig_y - height // 2 + image_center_y

                transformed_x, transformed_y = self.transform(
                    orig_screen_x, orig_screen_y
                )

                if (
                    0 <= transformed_x < self.screen_width
                    and 0 <= transformed_y < self.screen_height
                ):
                    dx = transformed_x - self.mirror_center_x
                    dy = transformed_y - self.mirror_center_y
                    distance_from_center = (dx * dx + dy * dy) ** 0.5

                    if (
                        distance_from_center <= self.mirror_radius
                        and transformed_x >= self.mirror_center_x
                    ):
                        pixel_colour = source_array[orig_x, orig_y]
                        transformed_surface.set_at(
                            (int(transformed_x), int(transformed_y)), pixel_colour
                        )

        return transformed_surface

    def draw_guide_rays(self, screen, image_rect, screen_width=None, screen_height=None):
        """Draw guide rays for convex mirror."""
        pixel_x, pixel_y = self._get_pixel_position(image_rect)
        
        ray_colour = (255, 0, 0)
        extension_colour = (255, 100, 100)
        intersection_colour = (255, 100, 100)
        ray_thickness = 2
        circle_radius = 4

        horizontal_hit = self._calculate_mirror_intersection_horizontal(pixel_x, pixel_y)
        focal_hit = self._calculate_mirror_intersection_focal(pixel_x, pixel_y)

        if horizontal_hit and focal_hit:
            # Draw incident rays (object -> hit)
            pygame.draw.line(screen, ray_colour, (pixel_x, pixel_y), horizontal_hit, ray_thickness)
            pygame.draw.line(screen, ray_colour, (pixel_x, pixel_y), focal_hit, ray_thickness)

            # Normalize incident vectors
            def _normalize(vx, vy):
                l = (vx * vx + vy * vy) ** 0.5
                return (vx / l, vy / l) if l > 0 else (0.0, 0.0)

            h_inc = _normalize(horizontal_hit[0] - pixel_x, horizontal_hit[1] - pixel_y)
            f_inc = _normalize(focal_hit[0] - pixel_x, focal_hit[1] - pixel_y)

            # Reflected directions using the true incident vectors
            horizontal_reflected = self._calculate_reflected_ray_direction(horizontal_hit, h_inc)
            focal_reflected = self._calculate_reflected_ray_direction(focal_hit, f_inc)

            # Draw reflected solid rays (to mirror boundary or screen edge)
            horizontal_end = self._calculate_reflected_end(horizontal_hit, horizontal_reflected)
            focal_end = self._calculate_reflected_end(focal_hit, focal_reflected)

            if horizontal_end:
                pygame.draw.line(screen, ray_colour, horizontal_hit, horizontal_end, ray_thickness)
            if focal_end:
                pygame.draw.line(screen, ray_colour, focal_hit, focal_end, ray_thickness)

            # Virtual extensions (dashed) and virtual-image intersection (unchanged)
            horizontal_extension_direction = (-horizontal_reflected[0], -horizontal_reflected[1])
            focal_extension_direction = (self.mirror_center_x - focal_hit[0], self.mirror_center_y - focal_hit[1])
            
            focal_ext_length = (focal_extension_direction[0] ** 2 + focal_extension_direction[1] ** 2) ** 0.5
            if focal_ext_length > 0:
                focal_extension_direction = (
                    focal_extension_direction[0] / focal_ext_length,
                    focal_extension_direction[1] / focal_ext_length,
                )

            extension_intersection = self.physics.calculate_ray_intersection(
                horizontal_hit, horizontal_extension_direction, focal_hit, focal_extension_direction
            )

            if extension_intersection:
                self.ray_drawer.draw_dashed_line(screen, horizontal_hit, extension_intersection, 
                                            extension_colour, ray_thickness)
                self.ray_drawer.draw_dashed_line(screen, focal_hit, extension_intersection, 
                                            extension_colour, ray_thickness)
                pygame.draw.circle(screen, intersection_colour, 
                                (int(extension_intersection[0]), int(extension_intersection[1])), circle_radius)
            else:
                # Fallback: draw extensions toward focal point
                self.ray_drawer.draw_dashed_line(screen, horizontal_hit, 
                                            (self.mirror_center_x, self.mirror_center_y), 
                                            extension_colour, ray_thickness)
                self.ray_drawer.draw_dashed_line(screen, focal_hit, 
                                            (self.mirror_center_x, self.mirror_center_y), 
                                            extension_colour, ray_thickness)
                pygame.draw.circle(screen, intersection_colour, 
                                (int(self.mirror_center_x), int(self.mirror_center_y)), circle_radius)

            pygame.draw.circle(screen, ray_colour, (int(pixel_x), int(pixel_y)), circle_radius)


# =============================================================================
# THIN LENS CLASS
# =============================================================================


class ThinLens(OpticalElement):
    """Thin lens transformation class."""

    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        self.lens_center_x = screen_width // 2
        self.lens_center_y = screen_height // 2
        self.focal_length = FOCAL_LENGTH

    def transform(self, world_x, world_y):
        """Thin lens: X = -f*x/(x-f), Y = y/x * X"""
        x_rel = world_x - self.lens_center_x
        y_rel = world_y - self.lens_center_y

        if abs(x_rel) < 2.0 or abs(x_rel - self.focal_length) < 2.0:
            return world_x, world_y

        try:
            X_rel = -self.focal_length * x_rel / (x_rel - self.focal_length)
            Y_rel = (y_rel / x_rel) * X_rel if abs(x_rel) > 2.0 else y_rel

            return X_rel + self.lens_center_x, Y_rel + self.lens_center_y
        except (ZeroDivisionError, OverflowError):
            return world_x, world_y

    def pixel_transformation(
        self, surface, image_center_pos, screen_width=None, screen_height=None
    ):
        """Apply thin lens transformation with pixel stretching for magnification."""
        width, height = surface.get_size()
        source_array = pygame.surfarray.array3d(surface)

        transformed_surface = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA
        )
        transformed_surface.fill((0, 0, 0, 0))

        image_center_x, image_center_y = image_center_pos
        half_width = width // 2
        focal_point_x = self.lens_center_x + self.focal_length

        # Check if image is in focal range (virtual image case)
        if self.lens_center_x < image_center_x <= focal_point_x:
            self._handle_virtual_image_transformation(
                source_array,
                transformed_surface,
                width,
                height,
                image_center_x,
                image_center_y,
                half_width,
                focal_point_x,
            )
        else:
            self._handle_real_image_transformation(
                source_array,
                transformed_surface,
                width,
                height,
                image_center_x,
                image_center_y,
                half_width,
                focal_point_x,
            )

        return transformed_surface

    def _handle_virtual_image_transformation(
        self,
        source_array,
        transformed_surface,
        width,
        height,
        image_center_x,
        image_center_y,
        half_width,
        focal_point_x,
    ):
        """Handle transformation for virtual image case."""
        for orig_x in range(width):
            for orig_y in range(height):
                orig_screen_x = orig_x - half_width + image_center_x
                orig_screen_y = orig_y - height // 2 + image_center_y

                distance_from_focal_line = abs(orig_screen_x - focal_point_x)
                if distance_from_focal_line < 5.0:
                    continue

                virtual_pos = self._calculate_virtual_image_position(
                    orig_screen_x, orig_screen_y
                )

                if virtual_pos:
                    virtual_x, virtual_y = virtual_pos

                    if (
                        0 <= virtual_x < self.screen_width
                        and 0 <= virtual_y < self.screen_height
                    ):
                        pixel_color = source_array[orig_x, orig_y]
                        distance_from_lens = abs(orig_screen_x - self.lens_center_x)

                        stretch_size = self._calculate_virtual_stretch_size(
                            distance_from_lens
                        )
                        self._apply_lens_pixel_stretching(
                            transformed_surface,
                            virtual_x,
                            virtual_y,
                            pixel_color,
                            stretch_size,
                        )

    def _handle_real_image_transformation(
        self,
        source_array,
        transformed_surface,
        width,
        height,
        image_center_x,
        image_center_y,
        half_width,
        focal_point_x,
    ):
        """Handle transformation for real image case."""
        for orig_x in range(width):
            for orig_y in range(height):
                orig_screen_x = orig_x - half_width + image_center_x
                orig_screen_y = orig_y - height // 2 + image_center_y

                distance_from_focal_line = abs(orig_screen_x - focal_point_x)
                if distance_from_focal_line < 5.0:
                    continue

                transformed_x, transformed_y = self.transform(
                    orig_screen_x, orig_screen_y
                )

                if not (
                    0 <= transformed_x < self.screen_width
                    and 0 <= transformed_y < self.screen_height
                ):
                    continue

                pixel_color = source_array[orig_x, orig_y]
                distance_from_lens = abs(orig_screen_x - self.lens_center_x)

                stretch_size = self._calculate_real_stretch_size(distance_from_lens)
                self._apply_lens_pixel_stretching(
                    transformed_surface,
                    transformed_x,
                    transformed_y,
                    pixel_color,
                    stretch_size,
                )

    def _calculate_virtual_stretch_size(self, distance_from_lens):
        """Calculate stretch size for virtual image."""
        if distance_from_lens > 0:
            virtual_magnification = abs(
                self.focal_length / (self.focal_length - distance_from_lens)
            )
            virtual_magnification = min(virtual_magnification, 20.0)

            focal_point_distance = (
                abs(distance_from_lens - self.focal_length) / self.focal_length
            )
            proximity_multiplier = 1.0 + (1.0 - focal_point_distance) * 3.0
            stretch_size = max(
                1, int(virtual_magnification * proximity_multiplier * 0.7)
            )
        else:
            stretch_size = 1

        return min(stretch_size, 25)

    def _calculate_real_stretch_size(self, distance_from_lens):
        """Calculate stretch size for real image."""
        if self.focal_length < distance_from_lens < 2 * self.focal_length:
            magnification = abs(
                self.focal_length / (self.focal_length - distance_from_lens)
            )
            magnification = min(magnification, 20.0)

            focal_point_distance = (
                abs(distance_from_lens - self.focal_length) / self.focal_length
            )
            proximity_multiplier = 1.0 + (1.0 - focal_point_distance) * 3.0
            stretch_size = max(1, int(magnification * proximity_multiplier * 0.7))
        elif distance_from_lens <= 1.75 * self.focal_length:
            base_stretch = 15
            center_proximity = 1.0 - (distance_from_lens / (1.75 * self.focal_length))
            stretch_size = max(1, int(base_stretch * (1.0 + center_proximity * 3.0)))
        else:
            stretch_size = 1

        return min(stretch_size, 25)

    def _apply_lens_pixel_stretching(
        self, surface, center_x, center_y, pixel_color, stretch_size
    ):
        """Apply enhanced pixel stretching for lens magnification."""
        center_x, center_y = int(center_x), int(center_y)

        # Calculate stretching parameters
        if stretch_size > 15:
            effective_stretch = stretch_size + 12
            gap_fill_radius = stretch_size + 6
            extra_fill_radius = stretch_size + 3
        elif stretch_size > 10:
            effective_stretch = stretch_size + 10
            gap_fill_radius = stretch_size + 5
            extra_fill_radius = stretch_size + 2
        elif stretch_size > 5:
            effective_stretch = stretch_size + 7
            gap_fill_radius = stretch_size + 3
            extra_fill_radius = stretch_size + 1
        else:
            effective_stretch = max(stretch_size + 3, 4)
            gap_fill_radius = stretch_size + 1
            extra_fill_radius = 0

        # Primary fill
        half_stretch = effective_stretch // 2
        half_stretch_y = max(half_stretch // 2, 1)  # Reduce vertical stretch

        for dx in range(-half_stretch, half_stretch + 1):
            for dy in range(-half_stretch_y, half_stretch_y + 1):
                pixel_x, pixel_y = center_x + dx, center_y + dy
                if (
                    0 <= pixel_x < self.screen_width
                    and 0 <= pixel_y < self.screen_height
                ):
                    surface.set_at((pixel_x, pixel_y), pixel_color)

        # Secondary and tertiary fills for high magnification
        if stretch_size > 6:
            self._apply_cross_pattern_fill(
                surface, center_x, center_y, pixel_color, gap_fill_radius
            )

        if stretch_size > 12:
            self._apply_extra_fill(
                surface, center_x, center_y, pixel_color, extra_fill_radius
            )

    def _apply_cross_pattern_fill(
        self, surface, center_x, center_y, pixel_color, gap_fill_radius
    ):
        """Apply cross pattern fill for medium magnification."""
        vertical_gap_radius = max(gap_fill_radius // 3, 1)

        for offset in range(1, gap_fill_radius + 1):
            # Extended horizontal lines
            for dx in range(-gap_fill_radius - 2, gap_fill_radius + 3):
                for dy_offset in [-offset, offset]:
                    if abs(dy_offset) <= vertical_gap_radius:
                        pixel_x = center_x + dx
                        pixel_y = center_y + dy_offset
                        if (
                            0 <= pixel_x < self.screen_width
                            and 0 <= pixel_y < self.screen_height
                        ):
                            surface.set_at((pixel_x, pixel_y), pixel_color)

            # Reduced vertical lines
            for dy in range(-vertical_gap_radius - 1, vertical_gap_radius + 2):
                for dx_offset in [-offset, offset]:
                    pixel_x = center_x + dx_offset
                    pixel_y = center_y + dy
                    if (
                        0 <= pixel_x < self.screen_width
                        and 0 <= pixel_y < self.screen_height
                    ):
                        surface.set_at((pixel_x, pixel_y), pixel_color)

    def _apply_extra_fill(
        self, surface, center_x, center_y, pixel_color, extra_fill_radius
    ):
        """Apply extra fill for extreme magnification cases."""
        reduced_vertical_radius = max(extra_fill_radius // 4, 1)

        for dx in range(-extra_fill_radius, extra_fill_radius + 1):
            for dy in range(-reduced_vertical_radius, reduced_vertical_radius + 1):
                for sub_x in [0, 0.5, -0.5]:
                    for sub_y in [0]:  # Horizontal emphasis only
                        pixel_x = int(center_x + dx + sub_x)
                        pixel_y = int(center_y + dy + sub_y)
                        if (
                            0 <= pixel_x < self.screen_width
                            and 0 <= pixel_y < self.screen_height
                        ):
                            surface.set_at((pixel_x, pixel_y), pixel_color)

    def get_position(self, original_center, screen_width=None, screen_height=None):
        """Calculate the center position of a thin lens transformed image."""
        orig_x, orig_y = original_center
        transformed_x, transformed_y = self.transform(orig_x, orig_y)

        transformed_x = max(MARGIN, min(self.screen_width - MARGIN, transformed_x))
        transformed_y = max(MARGIN, min(self.screen_height - MARGIN, transformed_y))

        return transformed_x, transformed_y

    def draw_reference_lines(self, screen, screen_width=None, screen_height=None):
        """Draw lens shape and focal point reference lines."""
        lens_color = (150, 150, 150)
        lens_thickness = 20

        # Draw biconvex lens shape
        for y in range(self.screen_height):
            y_norm = (y - self.screen_height // 2) / (self.screen_height // 2)
            y_norm = max(-1, min(1, y_norm))
            curve = lens_thickness * (1 - y_norm * y_norm) ** 0.5

            left_x, right_x = int(self.lens_center_x - curve), int(
                self.lens_center_x + curve
            )
            if 0 <= left_x < self.screen_width:
                pygame.draw.circle(screen, lens_color, (left_x, y), 1)
            if 0 <= right_x < self.screen_width:
                pygame.draw.circle(screen, lens_color, (right_x, y), 1)

        # Draw center reference line
        pygame.draw.line(
            screen,
            (100, 100, 100),
            (self.lens_center_x, 0),
            (self.lens_center_x, self.screen_height),
            1,
        )

        # Draw focal lines (dashed)
        focal_color = (100, 150, 100)
        self._draw_focal_lines(screen, focal_color)

    def _draw_focal_lines(self, screen, focal_color):
        """Draw dashed focal lines."""
        dash_length = 10
        gap_length = 10

        for focal_x in [
            self.lens_center_x + self.focal_length,
            self.lens_center_x - self.focal_length,
        ]:
            if 0 <= focal_x <= self.screen_width:
                y = 0
                while y < self.screen_height:
                    end_y = min(y + dash_length, self.screen_height)
                    pygame.draw.line(
                        screen, focal_color, (focal_x, y), (focal_x, end_y), 2
                    )
                    y += dash_length + gap_length

                # Add focal point label
                font = pygame.font.Font(None, 24)
                f_text = font.render("F", True, focal_color)
                screen.blit(f_text, (focal_x + 5, self.screen_height // 2))

    def draw_guide_rays(
        self, screen, image_rect, screen_width=None, screen_height=None
    ):
        """Draw guide rays for the center topmost pixel of the original image."""
        pixel_x, pixel_y = self._get_pixel_position(image_rect)

        focal_point_x = self.lens_center_x + self.focal_length
        ray_color = (255, 0, 0)
        virtual_ray_color = (255, 100, 100)
        ray_thickness = 2
        circle_radius = 3

        if pixel_x > focal_point_x:
            self._draw_real_image_rays(
                screen, pixel_x, pixel_y, ray_color, ray_thickness, circle_radius
            )
        elif self.lens_center_x < pixel_x <= focal_point_x:
            self._draw_virtual_image_rays(
                screen,
                pixel_x,
                pixel_y,
                ray_color,
                virtual_ray_color,
                ray_thickness,
                circle_radius,
            )

    def _draw_real_image_rays(
        self, screen, pixel_x, pixel_y, ray_color, ray_thickness, circle_radius
    ):
        """Draw rays for real image formation."""
        transformed_x, transformed_y = self.transform(pixel_x, pixel_y)

        # Ray 1: Horizontal ray to lens, then refracted
        pygame.draw.line(
            screen,
            ray_color,
            (pixel_x, pixel_y),
            (self.lens_center_x, pixel_y),
            ray_thickness,
        )

        if (
            0 <= transformed_x < self.screen_width
            and 0 <= transformed_y < self.screen_height
        ):
            pygame.draw.line(
                screen,
                ray_color,
                (self.lens_center_x, pixel_y),
                (transformed_x, transformed_y),
                ray_thickness,
            )
            pygame.draw.line(
                screen,
                ray_color,
                (pixel_x, pixel_y),
                (transformed_x, transformed_y),
                ray_thickness,
            )
            pygame.draw.circle(
                screen,
                ray_color,
                (int(transformed_x), int(transformed_y)),
                circle_radius,
            )
        else:
            # Draw to screen edges
            self._draw_rays_to_screen_edge(
                screen,
                pixel_x,
                pixel_y,
                transformed_x,
                transformed_y,
                ray_color,
                ray_thickness,
            )

        pygame.draw.circle(
            screen, ray_color, (int(pixel_x), int(pixel_y)), circle_radius
        )

    def _draw_virtual_image_rays(
        self,
        screen,
        pixel_x,
        pixel_y,
        ray_color,
        virtual_ray_color,
        ray_thickness,
        circle_radius,
    ):
        """Draw rays for virtual image formation (object inside focal length)."""
        # 1. Draw horizontal incident ray to lens plane
        lens_hit_h = (self.lens_center_x, pixel_y)
        pygame.draw.line(
            screen, ray_color, (pixel_x, pixel_y), lens_hit_h, ray_thickness
        )

        # 2. Draw center incident ray to lens centre
        lens_hit_c = (self.lens_center_x, self.lens_center_y)
        pygame.draw.line(
            screen, ray_color, (pixel_x, pixel_y), lens_hit_c, ray_thickness
        )

        # 3. Compute virtual image position
        virtual_pos = self._calculate_virtual_image_position(pixel_x, pixel_y)

        # 4. Physical refracted ray for horizontal ray: away from virtual image
        if virtual_pos:
            vx, vy = virtual_pos
            dir_x = lens_hit_h[0] - vx
            dir_y = lens_hit_h[1] - vy
            horiz_edge = self.ray_drawer.calculate_screen_edge_intersection(
                lens_hit_h[0],
                lens_hit_h[1],
                dir_x,
                dir_y,
                self.screen_width,
                self.screen_height,
            )
            if horiz_edge:
                pygame.draw.line(
                    screen, ray_color, lens_hit_h, horiz_edge, ray_thickness
                )

        # 5. Physical refracted ray for centre ray: straight continuation
        dir_x = lens_hit_c[0] - pixel_x
        dir_y = lens_hit_c[1] - pixel_y
        center_edge = self.ray_drawer.calculate_screen_edge_intersection(
            lens_hit_c[0],
            lens_hit_c[1],
            dir_x,
            dir_y,
            self.screen_width,
            self.screen_height,
        )
        if center_edge:
            pygame.draw.line(screen, ray_color, lens_hit_c, center_edge, ray_thickness)

        # 6. Dashed virtual extensions back toward virtual image
        if virtual_pos:
            vx, vy = virtual_pos
            self.ray_drawer.draw_dashed_line(
                screen,
                lens_hit_h,
                (int(vx), int(vy)),
                virtual_ray_color,
                ray_thickness,
                dash_length=10,
            )
            self.ray_drawer.draw_dashed_line(screen, (pixel_x, pixel_y), (int(vx), int(vy)),
                                 virtual_ray_color, ray_thickness, dash_length=10)
            pygame.draw.circle(
                screen, virtual_ray_color, (int(vx), int(vy)), circle_radius
            )

        # 7. Mark object point
        pygame.draw.circle(
            screen, ray_color, (int(pixel_x), int(pixel_y)), circle_radius
        )

    def _draw_rays_to_screen_edge(
        self,
        screen,
        pixel_x,
        pixel_y,
        transformed_x,
        transformed_y,
        ray_color,
        ray_thickness,
    ):
        """Draw rays to screen edge when transformed point is off-screen."""
        # Ray 1 refracted
        direction_x = transformed_x - self.lens_center_x
        direction_y = transformed_y - pixel_y
        edge_point = self.ray_drawer.calculate_screen_edge_intersection(
            self.lens_center_x,
            pixel_y,
            direction_x,
            direction_y,
            self.screen_width,
            self.screen_height,
        )
        if edge_point:
            pygame.draw.line(
                screen,
                ray_color,
                (self.lens_center_x, pixel_y),
                edge_point,
                ray_thickness,
            )

        # Ray 2 through center
        direction_x = transformed_x - pixel_x
        direction_y = transformed_y - pixel_y
        edge_point = self.ray_drawer.calculate_screen_edge_intersection(
            pixel_x,
            pixel_y,
            direction_x,
            direction_y,
            self.screen_width,
            self.screen_height,
        )
        if edge_point:
            pygame.draw.line(
                screen, ray_color, (pixel_x, pixel_y), edge_point, ray_thickness
            )

    def _draw_virtual_extensions(
        self,
        screen,
        pixel_x,
        pixel_y,
        virtual_x,
        virtual_y,
        virtual_ray_color,
        ray_thickness,
        circle_radius,
    ):
        """Draw virtual ray extensions."""
        if 0 <= virtual_x < self.screen_width and 0 <= virtual_y < self.screen_height:
            self.ray_drawer.draw_dashed_line(
                screen,
                (self.lens_center_x, pixel_y),
                (int(virtual_x), int(virtual_y)),
                virtual_ray_color,
                ray_thickness,
                dash_length=10,
            )
            self.ray_drawer.draw_dashed_line(
                screen,
                (pixel_x, pixel_y),
                (int(virtual_x), int(virtual_y)),
                virtual_ray_color,
                ray_thickness,
                dash_length=10,
            )
            pygame.draw.circle(
                screen,
                virtual_ray_color,
                (int(virtual_x), int(virtual_y)),
                circle_radius,
            )

    def _calculate_virtual_image_position(self, pixel_x, pixel_y):
        """Calculate the virtual image position using thin lens physics."""
        object_distance = pixel_x - self.lens_center_x

        if abs(object_distance - self.focal_length) < 1e-6:
            return None

        image_distance_reciprocal = (1.0 / self.focal_length) - (1.0 / object_distance)

        if abs(image_distance_reciprocal) > 1e-6:
            virtual_image_distance = 1.0 / image_distance_reciprocal
            magnification = -virtual_image_distance / object_distance

            virtual_x = self.lens_center_x - virtual_image_distance
            virtual_y = (
                self.lens_center_y + (pixel_y - self.lens_center_y) * magnification
            )

            return (virtual_x, virtual_y)
        return None


# =============================================================================
# APPLICATION MANAGEMENT CLASSES
# =============================================================================


class ImageManager:
    """Image loading and setup management class."""

    @staticmethod
    def load_and_setup_image():
        """Load the image and set it up with initial position."""
        image = pygame.image.load("Applied/Physics/BPhO/Figures/image.png").convert()
        image = pygame.transform.scale(
            image,
            (
                image.get_width() // IMAGE_SCALE_FACTOR,
                image.get_height() // IMAGE_SCALE_FACTOR,
            ),
        )

        initial_x = WINDOW_WIDTH * 3 // 4
        initial_y = WINDOW_HEIGHT // 2
        image_rect = image.get_rect(center=(initial_x, initial_y))

        return image, image_rect


class TransformationManager:
    """Manages all optical transformations."""

    def __init__(self, screen_width, screen_height):
        self.optical_elements = {
            "mirror": PlaneMirror(screen_width, screen_height),
            "lens": ThinLens(screen_width, screen_height),
            "concave": ConcaveMirror(screen_width, screen_height),
            "convex": ConvexMirror(screen_width, screen_height),
        }
        self.current_transformation = "mirror"

    def update_screen_size(self, screen_width, screen_height):
        """Update all optical elements with new screen dimensions."""
        self.optical_elements = {
            "mirror": PlaneMirror(screen_width, screen_height),
            "lens": ThinLens(screen_width, screen_height),
            "concave": ConcaveMirror(screen_width, screen_height),
            "convex": ConvexMirror(screen_width, screen_height),
        }

    def set_transformation_type(self, transformation_type):
        """Set the current transformation type."""
        self.current_transformation = transformation_type

    def get_current_element(self):
        """Get the current optical element."""
        return self.optical_elements.get(self.current_transformation)

    def apply_pixel_transformation(self, surface, image_center_pos, screen_size):
        """Apply the current transformation to every single pixel."""
        if self.current_transformation == "none":
            return surface

        element = self.get_current_element()
        if element:
            screen_width, screen_height = screen_size
            return element.pixel_transformation(
                surface, image_center_pos, screen_width, screen_height
            )
        return surface

    def get_transformed_position(self, original_center, screen_width, screen_height):
        """Calculate where the transformed image should be positioned."""
        if self.current_transformation == "none":
            return original_center

        element = self.get_current_element()
        if element:
            return element.get_position(original_center, screen_width, screen_height)
        return original_center

    def draw_reference_lines(self, screen, screen_width, screen_height):
        """Draw reference lines for the current transformation."""
        element = self.get_current_element()
        if element:
            element.draw_reference_lines(screen, screen_width, screen_height)

    def draw_guide_rays(self, screen, image_rect, screen_width, screen_height):
        """Draw guide rays for the current transformation."""
        element = self.get_current_element()
        if element:
            element.draw_guide_rays(screen, image_rect, screen_width, screen_height)


class MovementConstraints:
    """Handles movement constraints for different transformation types."""

    @staticmethod
    def apply_constraints(new_center, image, screen_size, transformation_type):
        """Apply movement constraints based on current transformation type."""
        screen_width, screen_height = screen_size
        image_width, image_height = image.get_size()

        # General window boundary constraints
        min_x, min_y = image_width // 2, image_height // 2
        max_x = screen_width - image_width // 2
        max_y = screen_height - image_height // 2 - 50

        constrained_x = max(min_x, min(max_x, new_center[0]))
        constrained_y = max(min_y, min(max_y, new_center[1]))

        # Transformation-specific constraints
        constraint_map = {
            "mirror": screen_width // 2 + image_width // 2 + 10,
            "lens": screen_width // 2 + image_width // 2 + 10,
            "concave": CONCAVE_MIRROR_RADIUS + 200 + image_width // 2 + 10,
            "convex": CONCAVE_MIRROR_RADIUS
            + 200
            + CONCAVE_MIRROR_RADIUS
            + image_width // 2
            + 10,
        }

        if transformation_type in constraint_map:
            constrained_x = max(constraint_map[transformation_type], constrained_x)

        return (constrained_x, constrained_y)


class EventHandler:
    """Event handling class for managing all user interactions."""

    def __init__(self, transformation_manager):
        self.transformation_manager = transformation_manager
        self.show_guide_rays = False

    def handle_window_resize(self, event, image_rect, prev_size):
        """Handle window resize events and adjust image position proportionally."""
        new_width, new_height = event.w, event.h
        old_width, old_height = prev_size

        width_scale = new_width / old_width
        height_scale = new_height / old_height

        old_center_x, old_center_y = image_rect.center
        new_center_x = int(old_center_x * width_scale)
        new_center_y = int(old_center_y * height_scale)
        image_rect.center = (new_center_x, new_center_y)

        self.transformation_manager.update_screen_size(new_width, new_height)
        return (new_width, new_height)

    def handle_fullscreen_toggle(self, key, current_fullscreen_state, screen):
        """Handle fullscreen toggle and return new state and screen."""
        if key == pygame.K_F11:
            new_state = not current_fullscreen_state
            new_screen = pygame.display.set_mode(
                (0, 0) if new_state else (WINDOW_WIDTH, WINDOW_HEIGHT),
                pygame.FULLSCREEN if new_state else pygame.RESIZABLE,
            )
            screen_size = new_screen.get_size()
            self.transformation_manager.update_screen_size(
                screen_size[0], screen_size[1]
            )
            print(f"Fullscreen: {'ON' if new_state else 'OFF'}")
            return new_state, new_screen
        elif key == pygame.K_ESCAPE and current_fullscreen_state:
            new_screen = pygame.display.set_mode(
                (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE
            )
            self.transformation_manager.update_screen_size(WINDOW_WIDTH, WINDOW_HEIGHT)
            print("Fullscreen: OFF")
            return False, new_screen
        return current_fullscreen_state, screen

    def handle_transformation_switch(self, key):
        """Handle transformation type switching."""
        transforms = {
            pygame.K_m: ("mirror", "plane mirror transformation"),
            pygame.K_l: ("lens", "thin lens transformation"),
            pygame.K_c: ("concave", "concave mirror transformation"),
            pygame.K_v: ("convex", "convex mirror transformation"),
            pygame.K_n: ("none", "no transformation"),
        }

        if key in transforms:
            transformation_type, description = transforms[key]
            self.transformation_manager.set_transformation_type(transformation_type)
            print(f"Switched to {description}")
            return True
        return False

    def handle_guide_ray_toggle(self, key):
        """Handle guide ray visibility toggle."""
        if key == pygame.K_r:
            self.show_guide_rays = not self.show_guide_rays
            print(f"Guide rays: {'ON' if self.show_guide_rays else 'OFF'}")
            return True
        return False

    def reset_image_to_initial_position(self, image_rect, screen_size):
        """Reset the image to its initial position."""
        screen_width, screen_height = screen_size
        initial_x = screen_width * 3 // 4
        initial_y = screen_height // 2
        image_rect.center = (initial_x, initial_y)

    def recalculate_transformation(self, image, image_rect, screen_size):
        """Recalculate the transformed image and position."""
        screen_width, screen_height = screen_size
        transformed_image = self.transformation_manager.apply_pixel_transformation(
            image, image_rect.center, screen_size
        )

        if self.transformation_manager.current_transformation in [
            "lens",
            "concave",
            "convex",
        ]:
            transformed_rect = pygame.Rect(0, 0, screen_width, screen_height)
        else:
            transformed_center = self.transformation_manager.get_transformed_position(
                image_rect.center, screen_width, screen_height
            )
            transformed_rect = transformed_image.get_rect(center=transformed_center)

        return transformed_image, transformed_rect


class RendererManager:
    """Rendering and drawing management class."""

    @staticmethod
    def draw_background_grid(screen, screen_width, screen_height):
        """Draw a soft grid in the background, centered on the screen."""
        grid_color = (60, 60, 60)
        grid_spacing = 50

        center_x = screen_width // 2
        center_y = screen_height // 2

        # Draw vertical lines
        x = center_x
        while x <= screen_width:
            pygame.draw.line(screen, grid_color, (x, 0), (x, screen_height), 1)
            x += grid_spacing

        x = center_x - grid_spacing
        while x >= 0:
            pygame.draw.line(screen, grid_color, (x, 0), (x, screen_height), 1)
            x -= grid_spacing

        # Draw horizontal lines
        y = center_y
        while y <= screen_height:
            pygame.draw.line(screen, grid_color, (0, y), (screen_width, y), 1)
            y += grid_spacing

        y = center_y - grid_spacing
        while y >= 0:
            pygame.draw.line(screen, grid_color, (0, y), (screen_width, y), 1)
            y -= grid_spacing

    @staticmethod
    def draw_images_and_labels(
        screen,
        image,
        image_rect,
        transformed_image,
        transformed_rect,
        transformation_type,
    ):
        """Draw images and their labels."""
        # Draw transformed image first (excluding certain types)
        if transformation_type not in ("none", "lens", "concave") and transformed_image:
            screen.blit(transformed_image, transformed_rect)

        # Draw original image on top
        screen.blit(image, image_rect)

        # Draw "Original" label
        font = pygame.font.Font(None, 36)
        orig_text = font.render("Original", True, (255, 255, 255))
        screen.blit(orig_text, (image_rect.centerx - 50, image_rect.bottom + 10))

    @staticmethod
    def draw_instructions(screen, transformation_type, show_guide_rays):
        """Draw instruction text."""
        font_small = pygame.font.Font(None, 24)
        instructions = [
            f"Current: {transformation_type.upper()} transformation",
            "M: Mirror | L: Lens | C: Concave Mirror | V: Convex Mirror | N: None | R: Toggle Guide Rays",
            "F11: Toggle Fullscreen | ESC: Exit Fullscreen",
        ]

        if transformation_type in ["lens", "concave", "convex"]:
            instructions.append(f"Guide rays: {'ON' if show_guide_rays else 'OFF'}")

        for i, instruction in enumerate(instructions):
            text = font_small.render(instruction, True, (200, 200, 200))
            screen.blit(text, (10, 10 + i * 25))


# =============================================================================
# MAIN APPLICATION CLASS
# =============================================================================


class OpticsSimulation:
    """Main application class that orchestrates the optics simulation."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE
        )
        pygame.display.set_caption("Interactive Optics Models")
        self.clock = pygame.time.Clock()

        self.transformation_manager = TransformationManager(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.event_handler = EventHandler(self.transformation_manager)
        self.renderer = RendererManager()
        self.movement_constraints = MovementConstraints()

        self.image, self.image_rect = ImageManager.load_and_setup_image()
        self.running = True
        self.dragging = False
        self.offset_x = self.offset_y = 0
        self.fullscreen = False
        self.prev_window_size = self.screen.get_size()

        print(
            f"Starting with {self.transformation_manager.current_transformation} transformation"
        )
        print("Controls: Drag original image around and release to see transformation")

        # Initial transformation calculation
        screen_size = self.screen.get_size()
        self.transformed_image, self.transformed_rect = (
            self.event_handler.recalculate_transformation(
                self.image, self.image_rect, screen_size
            )
        )

    def handle_events(self):
        """Handle all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.VIDEORESIZE:
                self.prev_window_size = self.event_handler.handle_window_resize(
                    event, self.image_rect, self.prev_window_size
                )
                screen_size = self.screen.get_size()
                self.transformed_image, self.transformed_rect = (
                    self.event_handler.recalculate_transformation(
                        self.image, self.image_rect, screen_size
                    )
                )

            elif event.type == pygame.KEYDOWN:
                self.fullscreen, self.screen = (
                    self.event_handler.handle_fullscreen_toggle(
                        event.key, self.fullscreen, self.screen
                    )
                )

                if self.event_handler.handle_transformation_switch(event.key):
                    screen_size = self.screen.get_size()
                    self.event_handler.reset_image_to_initial_position(
                        self.image_rect, screen_size
                    )
                    self.transformed_image, self.transformed_rect = (
                        self.event_handler.recalculate_transformation(
                            self.image, self.image_rect, screen_size
                        )
                    )

                self.event_handler.handle_guide_ray_toggle(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.image_rect.collidepoint(event.pos):
                    self.dragging = True
                    mouse_x, mouse_y = event.pos
                    self.offset_x = self.image_rect.centerx - mouse_x
                    self.offset_y = self.image_rect.centery - mouse_y

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.dragging:
                    self.dragging = False
                    screen_size = self.screen.get_size()
                    self.transformed_image, self.transformed_rect = (
                        self.event_handler.recalculate_transformation(
                            self.image, self.image_rect, screen_size
                        )
                    )

            elif event.type == pygame.MOUSEMOTION and self.dragging:
                mouse_x, mouse_y = event.pos
                new_center = (mouse_x + self.offset_x, mouse_y + self.offset_y)
                screen_size = self.screen.get_size()
                self.image_rect.center = self.movement_constraints.apply_constraints(
                    new_center,
                    self.image,
                    screen_size,
                    self.transformation_manager.current_transformation,
                )

    def render_frame(self):
        """Render a single frame."""
        self.screen.fill(BLACK)
        screen_size = self.screen.get_size()

        self.renderer.draw_background_grid(self.screen, *screen_size)
        self.transformation_manager.draw_reference_lines(self.screen, *screen_size)

        # Draw transformed image first (if lens, concave, or convex type)
        if (
            self.transformation_manager.current_transformation
            in ("lens", "concave", "convex")
            and self.transformed_image
        ):
            self.screen.blit(self.transformed_image, (0, 0))

        # Draw images and labels
        self.renderer.draw_images_and_labels(
            self.screen,
            self.image,
            self.image_rect,
            self.transformed_image,
            self.transformed_rect,
            self.transformation_manager.current_transformation,
        )

        # Draw guide rays if enabled
        if self.event_handler.show_guide_rays:
            self.transformation_manager.draw_guide_rays(
                self.screen, self.image_rect, *screen_size
            )

        self.renderer.draw_instructions(
            self.screen,
            self.transformation_manager.current_transformation,
            self.event_handler.show_guide_rays,
        )
        pygame.display.flip()

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.render_frame()
            self.clock.tick(FRAMERATE)

        pygame.quit()
        print("Program Exited")


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================


def main():
    """Main entry point."""
    simulation = OpticsSimulation()
    simulation.run()


if __name__ == "__main__":
    main()
