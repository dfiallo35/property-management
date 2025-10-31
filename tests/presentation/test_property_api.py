import pytest
from fastapi import status

from uuid import uuid4
from httpx import AsyncClient


class TestPropertyCreate:
    url = "/api/properties/"

    @pytest.mark.asyncio
    async def test_create_property_success(self, async_client: AsyncClient):
        response = await async_client.post(
            self.url,
            json={
                "property_type": "test",
                "room_count": 1,
                "bathroom_count": 1,
                "additional_features": ["feature1", "feature2"],
                "location": {
                    "latitude": 1.0,
                    "longitude": 1.0,
                    "address": "test",
                },
                "rent_value": 1.0,
            },
        )

        assert response.status_code == status.HTTP_201_CREATED


class TestPropertyGet:
    url = "/api/properties/{property_id}"

    @pytest.mark.asyncio
    async def test_get_property_success(
        self, async_client: AsyncClient, create_property
    ):
        response = await async_client.get(
            self.url.format(property_id=create_property.id),
        )

        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_get_property_not_found(self, async_client: AsyncClient):
        response = await async_client.get(
            self.url.format(property_id=uuid4()),
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestPropertyList:
    url = "/api/properties/"

    @pytest.mark.asyncio
    async def test_list_properties_success(
        self, async_client: AsyncClient, create_property
    ):
        response = await async_client.get(self.url, params={})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1


class TestPropertyUpdate:
    url = "/api/properties/{property_id}"

    @pytest.mark.asyncio
    async def test_update_property_success(
        self, async_client: AsyncClient, create_property
    ):
        response = await async_client.put(
            self.url.format(property_id=create_property.id),
            json={
                "room_count": 2,
                "bathroom_count": 2,
            },
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["room_count"] == 2
        assert response.json()["bathroom_count"] == 2

    @pytest.mark.asyncio
    async def test_update_property_not_found(self, async_client: AsyncClient):
        response = await async_client.put(
            self.url.format(property_id=uuid4()),
            json={
                "room_count": 2,
                "bathroom_count": 2,
            },
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestPropertyDelete:
    url = "/api/properties/{property_id}"

    @pytest.mark.asyncio
    async def test_delete_property_success(
        self, async_client: AsyncClient, create_property
    ):
        response = await async_client.delete(
            self.url.format(property_id=create_property.id),
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = await async_client.get(
            self.url.format(property_id=create_property.id),
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_delete_property_not_found(self, async_client: AsyncClient):
        response = await async_client.delete(
            self.url.format(property_id=uuid4()),
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
