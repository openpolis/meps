import scraperwiki
import lxml.html

euparl_url = "http://www.europarl.europa.eu"

# read list of meps
print("Reading list from EU Parliament web site")
html = scraperwiki.scrape(
    "{0}/meps/en/full-list.html?filter=all&leg=".format(euparl_url)
)

root = lxml.html.fromstring(html)
for div in root.cssselect("div[class='zone_info_mep ']"):
    mep_link = div.cssselect("li[class='mep_name'] a")[0]
    mep_name = mep_link.text
    mep_url = mep_link.attrib['href']

    mep_id = int(mep_url.split('/')[3])

    print(u"Reading mep data from {0}".format(mep_url))
    mep_html = scraperwiki.scrape(
        "{0}{1}".format(euparl_url, mep_url)
    )
    mep_root = lxml.html.fromstring(mep_html)

    mep_group = mep_root.cssselect(
        "#zone_before_content_global li.group"
    )[0].text.strip()

    try:
        mep_nationality = mep_root.cssselect(
            "#zone_before_content_global li.nationality"
        )[0].text.strip()
    except IndexError:
        mep_nationality = None

    try:
        mep_party = mep_root.cssselect(
            "#zone_before_content_global li.nationality span.name_pol_group"
        )[0].text.strip()
    except IndexError:
        mep_party = None

    try:
        (mep_birth_date, mep_birth_place) = mep_root.cssselect(
            "#zone_before_content_global li.nationality + span.more_info"
        )[0].text.strip().split(',', 1)
        mep_birth_date = mep_birth_date.replace('Date of birth: ', '')
        mep_birth_place = mep_birth_place.strip()
    except ValueError:
        mep_birth_date = None
        mep_birth_place = None

    try:
        image = mep_root.cssselect(
            "#zone_before_content_global > div > img"
        )[0].attrib['src']
    except IndexError:
        image = None

    try:
        feed = mep_root.cssselect(
            "#content_right > div.widget.socials > ul > li.rss > a"
        )[0].attrib['href']
    except IndexError:
        feed = None

    try:
        email = mep_root.cssselect("#email-0")[0].attrib['href'].replace(
            '[dot]', '.').replace('[at]', '@').replace("mailto:", "")[::-1]
    except IndexError:
        email = None

    try:
        website = mep_root.cssselect(
            "#content_right ul.link_collection_noborder "
            "li a.link_website"
        )[0].attrib['href']
    except IndexError:
        website = None

    try:
        facebook = mep_root.cssselect(
            "#content_right ul.link_collection_noborder "
            "li a.link_fb"
        )[0].attrib['href']
    except IndexError:
        facebook = None

    try:
        twitter = mep_root.cssselect(
            "#content_right ul.link_collection_noborder "
            "li a.link_twitt"
        )[0].attrib['href']
    except IndexError:
        twitter = None

    try:
        youtube = mep_root.cssselect(
            "#content_right ul.link_collection_noborder "
            "li a.link_youtube"
        )[0].attrib['href']
    except IndexError:
        youtube = None


    # write record out to the sqlite database
    scraperwiki.sqlite.save(
        unique_keys=['id'],
        data={
            "id": mep_id,
            "name": mep_name,
            "eu_url": "{0}{1}".format(euparl_url, mep_url),
            "group": mep_group,
            "nationality": mep_nationality,
            "party": mep_party,
            "birth_date": mep_birth_date,
            "birth_place": mep_birth_place,
            "image_url": "{0}{1}".format(euparl_url, image),
            "email": email,
            "website": website,
            "facebook": facebook,
            "twitter": twitter,
            "youtube": youtube
        }
    )
