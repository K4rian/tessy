"""
This script is used to generate the single-page documentation of a given module.

It hasn't been designed to be extensible nor pretty but only to fulfil some needs, use it 
at your own risk.

The output format is heavily inspired by some of BoppreH's projects (https://github.com/boppreh)
"""
import importlib
import inspect
import re


# TODO: Make this script invokable to be able to set all config variables dynamically
Config = type(
    "Config",
    (object,),
    {
        "TARGET_MODULE": importlib.import_module("tessy"),
        "OUTPUT_FILE": "README.md",
        "IGNORED_MEMBERS": ["VERSION"],
        "DEPOT_URL": "https://github.com/k4rian/tessy",
    },
)

Template = type(
    "Template",
    (object,),
    {
        "BODY": (
            "{module_doc}\n"
            "# API\n"
            "#### Table of Contents\n"
            "{members_toc}\n\n"
            "{members_info}"
        ),
        "MEMBER_TOC": "- [{parent_name}.**{name}**](#{link}) {alias}",
        "MEMBER_INFO": "## {name}{sign}\n{doc}\n",
        "MEMBER_INFO_SUB": "### {name}{sign}\n{doc}\n",
        "PREFIX_CLASS": "class {cls_name}",
        "SUFFIX_ALIAS": "*(alias)*",
        "SUFFIX_CLASS": "*(class)*",
    },
)

MemberInfo = type(
    "MemberInfo",
    (object,),
    {
        "obj": None,
        "name": "",
        "doc": "",
        "sign": "",
        "parent_name": "",
        "link": "",
        "is_class": False,
        "is_class_method": False,
        "is_enum": False,
        "is_enum_val": False,
        "is_str": False,
        "is_number": False,
        "is_alias": False,
    },
)

FORMATDATA = [
    # Replaces @@$ with member link
    {
        "REG_FINDALL": "\(@@\$(.*?)\)",
        "FMT_REPLACE_OLD": "@@${0}",
        "FMT_REPLACE_NEW": "{depot_url}#{link}",
        "FMT_REPLACE_USE_MEMBER_ATTRS": True,
        "MEMBER_ATTRS": ["link"],
    },
    # Replaces @@ with depot url
    {
        "REG_FINDALL": "@@(.*?)",
        "FMT_REPLACE_OLD": "@@{0}",
        "FMT_REPLACE_NEW": "{depot_url}{match}",
        "FMT_REPLACE_USE_MEMBER_ATTRS": False,
    },
]


def str_to_mdlink(s):
    s = re.sub("[.()'=*]", "", s)
    s = re.sub("[, ]", "-", s)
    s = s.replace("\\", "").replace("--", "-")

    return s.lower()


def format_doc(text, **kw):
    result = text.strip()

    for fmt in FORMATDATA:
        find_result = re.findall(fmt["REG_FINDALL"], text, flags=re.MULTILINE)

        if len(find_result) > 0:
            for match in find_result:
                repl_old = fmt["FMT_REPLACE_OLD"]
                repl_new = fmt["FMT_REPLACE_NEW"]
                repl_kw = dict(kw.items())

                if "{match}" in repl_new:
                    repl_kw["match"] = match

                if fmt["FMT_REPLACE_USE_MEMBER_ATTRS"]:
                    member = get_member_info(match)

                    for attr_name in fmt["MEMBER_ATTRS"]:
                        attr_val = (
                            getattr(member, attr_name)
                            if hasattr(member, attr_name)
                            else None
                        )
                        repl_kw[attr_name] = attr_val if attr_val else ""

                result = result.replace(
                    repl_old.format(match), repl_new.format(**repl_kw)
                )

    return result


def get_members_info(obj):
    result = []
    attrs = obj.__dict__.keys()

    for attr_name in attrs:
        if attr_name.startswith("_") or attr_name in Config.IGNORED_MEMBERS:
            continue

        attr = getattr(obj, attr_name)

        if attr.__doc__:
            attr_str = str(attr)
            attr_type_str = str(type(attr))

            info = MemberInfo()
            info.obj = attr
            info.name = attr_name.strip()
            info.doc = inspect.getdoc(attr)
            info.parent_name = obj.__name__
            info.is_class = "class" in attr_str
            info.is_class_method = attr_str.startswith("<bound method")
            info.is_enum = "enum" in attr_type_str
            info.is_enum_val = info.is_enum and not attr_str.endswith("'>")
            info.is_str = isinstance(attr, str)
            info.is_number = isinstance(attr, (int, float))
            info.is_alias = info.doc.lower().startswith("alias")

            try:
                info.sign = str(inspect.signature(attr))
            except:
                pass

            info.link = str_to_mdlink(
                "{0}.{1}{2}".format(
                    info.parent_name, info.name, info.sign if not info.is_enum else ""
                )
            )

            result.append(info)

    return result


def get_member_info(member_name):
    result = [
        member
        for member in list(
            map(
                lambda m: m if m.name == member_name else None,
                get_members_info(Config.TARGET_MODULE),
            )
        )
        if member
    ]
    return result[0] if result else None


def build_member_doc(mi, is_sub=False):
    # nameA.nameB -> nameB
    parent_name = "".join(mi.parent_name.split(".")[-1:])

    # Format the name as displayed in the documentation
    formatted_name = "{0}.{1}".format(parent_name, mi.name)

    # Suffix any alias function (only visible in the TOC)
    alias = Template.SUFFIX_ALIAS if mi.is_alias else ""

    # Member's signature
    sign = ""

    # If its a class, use both a prefix and a suffix
    if mi.is_class:
        formatted_name = Template.PREFIX_CLASS.format(cls_name=mi.name)
        alias = Template.SUFFIX_CLASS

    # Don't display the signature if the member is an enum
    if not mi.is_enum:
        # Clean the signature
        sign = mi.sign.replace("self, ", "").replace(", /)", ")")

    # Member's raw documentation
    doc = ""

    # Member's TOC entry
    toc = ""

    # Documentation template to use
    info_tpl = Template.MEMBER_INFO_SUB if is_sub else Template.MEMBER_INFO

    # Member's formatted documentation
    info = ""

    # Display the value as doc if the member holds a number or a string
    if mi.is_str or mi.is_number or mi.is_enum_val:
        doc = "> = {0}".format(
            '"{0}"'.format(str(mi.obj)) if mi.is_str or mi.is_enum_val else str(mi.obj)
        )
    else:
        doc = "\n".join(mi.doc.splitlines())

    # Sub members aren't displayed in the TOC, only in the doc
    if not is_sub:
        toc = Template.MEMBER_TOC.format(
            parent_name=parent_name, name=mi.name, link=mi.link, alias=alias
        )

    info = info_tpl.format(link=mi.link, name=formatted_name, sign=sign, doc=doc)

    return (toc, info)


def build():
    module_doc = Config.TARGET_MODULE.__doc__
    build_tocs = []
    build_infos = []

    members_info = get_members_info(Config.TARGET_MODULE)
    for member in members_info:
        (m_toc, m_info) = build_member_doc(member)
        build_tocs.append(m_toc)
        build_infos.append(m_info)

        if member.is_class or member.is_enum:
            sub_members_info = get_members_info(member.obj)
            for sub_member in sub_members_info:
                (_, sm_info) = build_member_doc(sub_member, True)
                build_infos.append(sm_info)

    module_doc = format_doc(module_doc, depot_url=Config.DEPOT_URL)

    for idx, bi in enumerate(build_infos):
        build_infos[idx] = format_doc(bi, depot_url=Config.DEPOT_URL)

    doc = Template.BODY.format(
        module_doc=module_doc,
        members_toc="\n".join(build_tocs),
        members_info="\n".join(build_infos),
    )

    with open(Config.OUTPUT_FILE, "w") as f:
        f.write(doc)


build()
