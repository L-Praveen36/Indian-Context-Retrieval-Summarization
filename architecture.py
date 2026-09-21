from manim import *

class Task3Architecture(Scene):
    def construct(self):
        # 1. The Title Sequence
        title = Text("Task 3: Intelligent Routing & OCR", color=BLUE, weight=BOLD).scale(0.8)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # 2. Draw the Architecture Nodes
        # Router Node
        router_box = RoundedRectangle(corner_radius=0.2, color=PURPLE, height=1.5, width=3)
        router_text = Text("Density Router").scale(0.5)
        router = VGroup(router_box, router_text).move_to(LEFT * 4)

        # PyMuPDF Node
        direct_box = RoundedRectangle(corner_radius=0.2, color=GREEN, height=1.5, width=3)
        direct_text = Text("Direct Extraction\n(PyMuPDF)").scale(0.4)
        direct = VGroup(direct_box, direct_text).move_to(RIGHT * 3 + UP * 2)

        # OpenCV/Tesseract Node
        ocr_box = RoundedRectangle(corner_radius=0.2, color=RED, height=1.5, width=3)
        ocr_text = Text("3-Path OCR Engine\n(OpenCV + Tesseract)").scale(0.4)
        ocr = VGroup(ocr_box, ocr_text).move_to(RIGHT * 3 + DOWN * 2)

        # Animate the nodes appearing
        self.play(SpinInFromNothing(router), FadeIn(direct, shift=UP), FadeIn(ocr, shift=DOWN))

        # 3. Draw Connecting Paths
        arrow_direct = Arrow(router.get_right(), direct.get_left(), buff=0.1, color=GREEN)
        arrow_ocr = Arrow(router.get_right(), ocr.get_left(), buff=0.1, color=RED)
        self.play(GrowArrow(arrow_direct), GrowArrow(arrow_ocr))

        # 4. The Incoming Document Payload
        doc = Rectangle(height=0.8, width=0.6, color=WHITE, fill_opacity=0.2)
        doc_label = Text("PDF").scale(0.3).move_to(doc.get_center())
        payload = VGroup(doc, doc_label).move_to(LEFT * 7)

        self.play(FadeIn(payload, shift=RIGHT))
        
        # Document travels to Router
        self.play(payload.animate.move_to(router.get_center()), run_time=1.5)

        # 5. X-Ray Scanning Effect (Calculating Text Density)
        laser = Line(payload.get_top() + LEFT*0.4, payload.get_top() + RIGHT*0.4, color=YELLOW)
        self.play(Create(laser))
        self.play(laser.animate.move_to(payload.get_bottom()), run_time=1.5, rate_func=there_and_back)
        self.play(FadeOut(laser))

        # Router makes a decision (Glows to indicate processing)
        self.play(Circumscribe(router, color=YELLOW, time_width=2))
        
        # Payload turns red (identified as a scanned image)
        self.play(payload.animate.set_color(RED))
        
        # 6. Move payload along path to OCR Engine
        self.play(payload.animate.move_to(ocr.get_center()), run_time=1.5)
        self.play(FadeOut(payload))
        
        # 7. The 3-Path Split Visualization (Inside the OCR Box)
        sub_otsu = Text("[Path 1: Otsu]", color=YELLOW).scale(0.3).move_to(ocr.get_center() + UP*0.4)
        sub_adapt = Text("[Path 2: Adaptive]", color=YELLOW).scale(0.3).move_to(ocr.get_center())
        sub_raw = Text("[Path 3: Raw]", color=YELLOW).scale(0.3).move_to(ocr.get_center() + DOWN*0.4)
        
        # Hide main text, reveal the 3 parallel processes
        self.play(FadeOut(ocr_text))
        self.play(Write(sub_otsu), Write(sub_adapt), Write(sub_raw))
        
        # Pulse them to simulate concurrent processing
        self.play(Indicate(sub_otsu), Indicate(sub_adapt), Indicate(sub_raw))
        self.play(FadeOut(sub_otsu), FadeOut(sub_adapt), FadeOut(sub_raw))
        self.play(FadeIn(ocr_text))
        
        # 8. Output the Final JSON Result
        final_text = Text("{ 'text': 'Extracted Clean Output', 'confidence': 92% }", font="monospace", color=GREEN).scale(0.4)
        final_text.move_to(DOWN * 3.5)
        
        # The text shoots out from the OCR box
        self.play(TransformFromCopy(ocr_box, final_text))
        
        # Final success glow
        self.play(Circumscribe(final_text, color=GREEN, time_width=2))
        self.wait(3)