import asyncio
from pathlib import Path
from typing import List

import httpx
from rdflib import URIRef
from rdflib.namespace import SKOS
from rich.progress import track

from dawe_nrm import api
from dawe_nrm.graph import NRM, create_graph, serialize
from dawe_nrm.schemas import LUTSchema


def write_all(path: Path):
    new_line = "# Do not edit this file directly. This file is generated by `make luts` with endpoints from src/dawe_nrm/api/categorical_values/endpoints.py\n"

    top_level_collection_member_graph = create_graph()
    top_level_collection_uri = URIRef(
        "https://linked.data.gov.au/def/nrm/05f83f99-1998-4d11-8837-bb4a68788521"
    )

    async def generate(lut_endpoint: LUTSchema, client: httpx.Client):
        try:
            graph = await api.categorical_values.get(NRM, lut_endpoint, client)
            label = "-".join(lut_endpoint.label.split(" ")[:-1]).lower() + ".ttl"
            if label == "collection.ttl":
                raise ValueError(
                    "Categorical values collection cannot be named collection.ttl as it is already reserved for the top-level collection."
                )
            serialize(path / label, graph)

            with open(path / label, "r+") as file:
                content = file.read()
                file.seek(0)
                file.write(new_line + content)

            top_level_collection_member_graph.add(
                (
                    top_level_collection_uri,
                    SKOS.member,
                    NRM[lut_endpoint.collection_uuid],
                )
            )
        except api.categorical_values.exceptions.NoDataInAPIException as err:
            raise Exception(err) from err

    async def fetch_and_write(endpoints: List[LUTSchema]):
        async with httpx.AsyncClient(timeout=120) as client:
            tasks = [generate(endpoint, client) for endpoint in endpoints]
            for task in track(
                asyncio.as_completed(tasks),
                description=f"Pulling and writing LUTs to {path.absolute()}",
                total=len(endpoints),
            ):
                await task

    asyncio.run(fetch_and_write(api.categorical_values.endpoints))

    serialize(path / "collection-members.ttl", top_level_collection_member_graph)

    with open(path / "collection-members.ttl", "r+") as file:
        content = file.read()
        file.seek(0)
        file.write(new_line + content)
