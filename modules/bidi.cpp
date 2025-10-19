#include "bidi.h"
#include <fribidi/fribidi.h>
#include <iostream>

void BidiCharSanitizer::sanitize(std::vector<char32_t> &text)
{
    if (text.empty())
        return;

    FriBidiParType par_type = FRIBIDI_PAR_ON; 
    FriBidiCharType *bidi_types = new FriBidiCharType[text.size()];
    FriBidiLevel *embedding_levels = new FriBidiLevel[text.size()];

    FriBidiChar *buf = reinterpret_cast<FriBidiChar *>(text.data());

    fribidi_get_bidi_types(buf, text.size(), bidi_types);

    fribidi_get_par_embedding_levels(bidi_types, text.size(), &par_type, embedding_levels);

    fribidi_log2vis(
        buf,         
        text.size(), 
        &par_type,   
        buf,          
        nullptr,     
        nullptr,
        nullptr);

    delete[] bidi_types;
    delete[] embedding_levels;
}