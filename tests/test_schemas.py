from db.models.section import Section
from db.schemas.section import SectionSchema

top = Section(
    id=0,
    title="Top",
    path="0",
    children=[
        Section(
            id=1,
            title="Middle",
            path="0.1",
            children=[
                Section(id=2, title="Bottom", path="0.1.1", children=[])
            ],
        ),
        Section(
            id=3,
            title="Middle2",
            path="0.2",
            children=[
                Section(id=4, title="Bottom2", path="0.2.1", children=[])
            ],
        ),
    ],
)


def test_section_serialiser():
    serialiser = SectionSchema()
    result = serialiser.dump(top)
    assert len(result["children"]) == 2
    assert result["title"] == "Top"
    assert result["children"][0]["title"] == "Middle"
