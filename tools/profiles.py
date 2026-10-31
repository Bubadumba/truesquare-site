"""TrueSquare profiles on other sites (owner 30.10): one list for the footer and the schema sameAs.
FOOTER = shown in the footer of every page; EXTRA = only in sameAs. Add Yelp / BBB / Yellow Pages here when the owner sends the links."""

FOOTER = [
    ("Google", "https://www.google.com/maps?cid=7556474326958598816"),
    ("Facebook", "https://www.facebook.com/884791761377065"),
    ("Instagram", "https://www.instagram.com/truesquare.remodel/"),
    ("YouTube", "https://www.youtube.com/@truesquareremodel"),
    ("Houzz", "https://www.houzz.com/pro/serhii-tomilov"),
    ("Nextdoor", "https://nextdoor.com/page/truesquare-remodel-llc/"),
    ("Thumbtack", "https://www.thumbtack.com/wa/seattle/bathroom-remodeling/truesquare-remodel-llc/service/562919809761304593"),
]
EXTRA = [
    ("Pinterest", "https://www.pinterest.com/truesquareremodel/"),
    ("BuildZoom", "https://www.buildzoom.com/contractor/truesquare-remodel-llc-seattle-wa"),
    ("HomeGuide", "https://homeguide.com/wa/seattle/bathroom-remodeling/truesquare-remodel-llc-IQKRMBLXTC"),
    ("Foursquare", "https://foursquare.com/v/truesquare-remodel/6ae5311cda29955db34f2095"),
]
SAME_AS = [u for _, u in FOOTER + EXTRA]


def footer_links(sep=""):
    return sep.join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in FOOTER)
