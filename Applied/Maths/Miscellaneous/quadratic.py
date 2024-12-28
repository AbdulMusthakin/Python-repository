from manim import *


class QuadraticFormulaDerivation(Scene):

    def construct(self):

        title = (
            Text("Quadratic Formula Derivation")
            .to_edge(UP)
            .set_color_by_gradient(PINK, PURPLE)
        )
        self.play(Write(title), run_time=2)
        self.wait(0.5)

        def index_transform(self, source, target, transform_index):

            self.play(
                *[
                    (
                        ReplacementTransform(source[i], target[j])
                        if type(i) is int
                        else (
                            ReplacementTransform(source[int(i[1:])].copy(), target[j])
                            if i[0] == "r"
                            else (
                                FadeTransform(source[int(i[2:])].copy(), target[j])
                                if i[:2] == "fr"
                                else (
                                    FadeTransform(source[int(i[1:])], target[j])
                                    if i[0] == "f"
                                    else (
                                        FadeIn(target[j])
                                        if i[0] == "n"
                                        else FadeOut(source[int(i[1:])])
                                    )
                                )
                            )
                        )
                    )
                    for i, j in zip(*transform_index)
                ],
            )
            self.wait()

        eq1 = MathTex("ax^2 + bx + c = 0")[0]
        eq2 = MathTex("x^2 + \\frac{b}{a}x + \\frac{c}{a} = 0")[0]
        eq3 = MathTex("x^2 + \\frac{b}{a}x = -\\frac{c}{a}")[0]
        eq4 = MathTex(
            "x^2 + \\frac{b}{a}x + \\left(\\frac{b}{2a}\\right)^2 = \\left(\\frac{b}{2a}\\right)^2 -\\frac{c}{a}"
        )[0]
        eq5 = MathTex(
            "\\left(x + \\frac{b}{2a}\\right)^2 = \\left(\\frac{b}{2a}\\right)^2 -\\frac{c}{a}"
        )[0]
        eq6 = MathTex(
            "\\left(x + \\frac{b}{2a}\\right)^2 = \\frac{b^2}{4a^2} -\\frac{4ac}{4a^2}"
        )[0]
        eq7 = MathTex("\\left(x + \\frac{b}{2a}\\right)^2 = \\frac{b^2 - 4ac}{4a^2}")[0]
        eq8 = MathTex("x + \\frac{b}{2a} = \\pm\\sqrt{\\frac{b^2 - 4ac}{4a^2}}")[0]
        eq9 = MathTex("x + \\frac{b}{2a} =  \\pm\\frac{\\sqrt{b^2 - 4ac}}{2a}")[0]
        eq10 = MathTex("x = - \\frac{b}{2a}  \\pm\\frac{\\sqrt{b^2 - 4ac}}{2a}")[0]
        eq11 = MathTex("x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}")[0]

        ti_1_2 = [
            ["f0", "fr0", 1, 2, 3, "r3", 4, 5, 6, "r6", 7, 8, 9],
            [5, 10, 0, 1, 2, 4, 3, 6, 7, 9, 8, 11, 12],
        ]
        ti_2_3 = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, "f12"],
            [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 7, 7],
        ]
        ti_3_4 = [
            [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                "n6",
                "n6",
                "n6",
                "n6",
                "n6",
                "n6",
                "n6",
                "n6",
                7,
                "n7",
                "n7",
                "n7",
                "n7",
                "n7",
                "n7",
                "n7",
                8,
                9,
                10,
                11,
            ],
            [i for i in range(0, 27)],
        ]
        ti_4_5 = [
            [
                "f0",
                "f1",
                2,
                "d3",
                "d4",
                "d5",
                "d6",
                "f7",
                "f8",
                9,
                10,
                11,
                12,
                13,
                "f14",
                15,
                16,
                17,
                18,
                19,
                20,
                21,
                22,
                23,
                24,
                25,
                26,
            ],
            [
                1,
                8,
                2,
                100,
                100,
                100,
                100,
                2,
                0,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
                20,
            ],
        ]
        ti_5_6 = [
            [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                "d10",
                11,
                12,
                13,
                14,
                "d15",
                16,
                "fr16",
                17,
                18,
                19,
                20,
                "fr20",
                "r20",
                "n20",
                "n20",
            ],
            [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                100,
                10,
                12,
                13,
                14,
                100,
                11,
                15,
                16,
                19,
                20,
                22,
                18,
                23,
                17,
                21,
            ],
        ]
        ti_6_7 = [
            [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                "f12",
                "f13",
                "f14",
                "f15",
                16,
                17,
                18,
                19,
                "f20",
                "f21",
                "f22",
                "f23",
            ],
            [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                16,
                17,
                18,
                19,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
            ],
        ]
        ti_7_8 = [
            [
                "d0",
                "f1",
                2,
                3,
                4,
                5,
                6,
                "d7",
                "d8",
                9,
                "n9",
                "n9",
                "n9",
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
            ],
            [
                100,
                0,
                1,
                2,
                3,
                4,
                5,
                100,
                100,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
            ],
        ]
        ti_8_9 = [
            [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                "f16",
                17,
                18,
                "d19",
            ],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 100],
        ]
        ti_9_10 = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            [0, 2, 3, 4, 5, 6, 1, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
        ]
        ti_10_11 = [
            [
                0,
                1,
                2,
                3,
                "f4",
                "f5",
                "f6",
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                "f16",
                "f17",
                "f18",
            ],
            [0, 1, 2, 3, 13, 14, 15, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        ]

        VGroup(eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9, eq10, eq11).scale(1.5)
        self.play(Write(eq1))
        self.wait()

        index_transform(self, eq1, eq2, ti_1_2)
        index_transform(self, eq2, eq3, ti_2_3)
        index_transform(self, eq3, eq4, ti_3_4)
        index_transform(self, eq4, eq5, ti_4_5)
        index_transform(self, eq5, eq6, ti_5_6)
        index_transform(self, eq6, eq7, ti_6_7)
        index_transform(self, eq7, eq8, ti_7_8)
        index_transform(self, eq8, eq9, ti_8_9)
        index_transform(self, eq9, eq10, ti_9_10)
        index_transform(self, eq10, eq11, ti_10_11)


class IndexIdentify(Scene):
    def construct(self):
        from itertools import cycle

        def get_sub_indexes(tex):
            ni = VGroup()
            colors = cycle([RED, TEAL, GREEN, BLUE, PURPLE])
            for i in range(len(tex)):
                n = Text(f"{i}", color=next(colors)).scale(0.7)
                n.next_to(tex[i], DOWN, buff=0.01)
                ni.add(n)
            return ni

        target = MathTex("x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}")[0]
        source = MathTex("x = - \\frac{b}{2a}  \\pm\\frac{\\sqrt{b^2 - 4ac}}{2a}")[0]

        VGroup(source, target).scale(1.5).arrange(DOWN, buff=2)
        source_ind = get_sub_indexes(source)
        target_ind = get_sub_indexes(target)

        self.add(source, source_ind, target, target_ind)
