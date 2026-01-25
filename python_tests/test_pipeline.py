import pytest
import random
import string
from python.generate_attack import (
    TagAttack,
    VariationSelectorAttack,
    InvisibleCharAttack,
    HomoglyphAttack,
    DeletionCharAttack,
    BidiAttack,
)

try:
    import textual_adversarial_defense
except ImportError:
    pytest.skip(
        "textual_adversarial_defense package not available", allow_module_level=True
    )


class TestCombinedAttacks:
    def test_combined_sanitizer(self):
        perturbed = """ 1fH$!ZM9󠅰󠄸⁠T-B#rKrm<G'{:sNm~​ϳ^Q8*󠁬mT3O;>A)94󠁲%Hh)bl}Z{\=a;"QF~Ρ{󠅭iy󠆗+C󠁧Es(5lkO$!nM󠁘)󠇉L{p)Q(A:).K︎⁠4󠁹l/XO,EL‭⁦‮⁦y⁩⁦x⁩‬⁩‬xe;[H8il]qtek`(^Y{&J%EB].1-J5"‌[?`Tk‍P;o󠄦!.=󠁚QyFc‍󠀲⁠~Io{CV󠄽‭⁦‮⁦Q⁩⁦v⁩‬⁩‬2h󠁈‭⁦‮⁦s⁩⁦m⁩‬⁩‬`C󠁤f,>':^jdp>y󠀾:,p​YlVoe:cyx|p󠇥9󠇙A~һ]c(2<m‭⁦‮⁦i⁩⁦H⁩‬⁩‬Cj?MS3"""
        expected = """ 1fH$!ZM9T-B#rKrm<G'{:sNm~j^Q8*mT3O;>A)94%Hh)bl}Z{\=a;"QF~P{iy+CEs(5lkO$!nM)L{p)Q(A:).K4l/XO,ELxyxe;[H8il]qtek`(^Y{&J%EB].1-J5"[?`TkP;o!.=QyFc~Io{CVvQ2hms`Cf,>':^jdp>y:,pYlVoe:cyx|p9A~h]c(2<mHiCj?MS3"""
        p_bidi_combined = textual_adversarial_defense._pipeline.Pipeline()
        p_bidi_combined.add_bidi_sanitizer()
        p_bidi_combined.add_combined_sanitizer()
        p_bidi_combined.add_deletion_sanitizer()

        result = p_bidi_combined.sanitize(perturbed)
        assert result == expected, f"Expected '{expected}', got '{result}'."

    def test_separate_sanitizers(self):
        perturbed = """ 1fH$!ZM9󠅰󠄸⁠T-B#rKrm<G'{:sNm~​ϳ^Q8*󠁬mT3O;>A)94󠁲%Hh)bl}Z{\=a;"QF~Ρ{󠅭iy󠆗+C󠁧Es(5lkO$!nM󠁘)󠇉L{p)Q(A:).K︎⁠4󠁹l/XO,EL‭⁦‮⁦y⁩⁦x⁩‬⁩‬xe;[H8il]qtek`(^Y{&J%EB].1-J5"‌[?`Tk‍P;o󠄦!.=󠁚QyFc‍󠀲⁠~Io{CV󠄽‭⁦‮⁦Q⁩⁦v⁩‬⁩‬2h󠁈‭⁦‮⁦s⁩⁦m⁩‬⁩‬`C󠁤f,>':^jdp>y󠀾:,p​YlVoe:cyx|p󠇥9󠇙A~һ]c(2<m‭⁦‮⁦i⁩⁦H⁩‬⁩‬Cj?MS3"""
        expected = """ 1fH$!ZM9T-B#rKrm<G'{:sNm~j^Q8*mT3O;>A)94%Hh)bl}Z{\=a;"QF~P{iy+CEs(5lkO$!nM)L{p)Q(A:).K4l/XO,ELxyxe;[H8il]qtek`(^Y{&J%EB].1-J5"[?`TkP;o!.=QyFc~Io{CVvQ2hms`Cf,>':^jdp>y:,pYlVoe:cyx|p9A~h]c(2<mHiCj?MS3"""

        p_all = textual_adversarial_defense._pipeline.Pipeline()
        p_all.add_bidi_sanitizer()
        p_all.add_tag_sanitizer()
        p_all.add_variation_selector_sanitizer()
        p_all.add_invisible_sanitizer()
        p_all.add_homoglyph_sanitizer()
        p_all.add_deletion_sanitizer()

        result = p_all.sanitize(perturbed)
        assert result == expected, f"Expected '{expected}', got '{result}'."
