import pytest
from fastapi import status

from uuid import uuid4
from httpx import AsyncClient

from property.domain.enums import ConfigurationType


class TestConfigurationCreate:
    url = "/api/properties/settings/"

    @pytest.mark.asyncio
    async def test_create_configuration_select_success(self, async_client: AsyncClient):
        response = await async_client.post(
            self.url,
            json={
                "key": "test",
                "type": ConfigurationType.SELECT.value,
                "value": ["test1", "test2"],
            },
        )

        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.asyncio
    async def test_create_configuration_number_success(self, async_client: AsyncClient):
        response = await async_client.post(
            self.url,
            json={
                "key": "test",
                "type": ConfigurationType.NUMBER.value,
            },
        )

        assert response.status_code == status.HTTP_201_CREATED


class TestConfigurationGet:
    url = "/api/properties/settings/{configuration_id}"

    @pytest.mark.asyncio
    async def test_get_configuration_success(
        self, async_client: AsyncClient, create_configuration
    ):
        response = await async_client.get(
            self.url.format(configuration_id=create_configuration.id),
        )

        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_get_configuration_not_found(self, async_client: AsyncClient):
        response = await async_client.get(
            self.url.format(configuration_id=uuid4()),
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestConfigurationList:
    url = "/api/properties/settings/"

    @pytest.mark.asyncio
    async def test_list_configurations_success(
        self, async_client: AsyncClient, create_configuration
    ):
        response = await async_client.get(self.url, params={})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1


class TestConfigurationUpdate:
    url = "/api/properties/settings/{configuration_id}"

    @pytest.mark.asyncio
    async def test_update_configuration_success(
        self, async_client: AsyncClient, create_configuration
    ):
        response = await async_client.put(
            self.url.format(configuration_id=create_configuration.id),
            json={
                "key": "test2",
            },
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["key"] == "test2"

    @pytest.mark.asyncio
    async def test_update_configuration_not_found(self, async_client: AsyncClient):
        response = await async_client.put(
            self.url.format(configuration_id=uuid4()),
            json={
                "key": "test2",
            },
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_update_configuration_not_valid_type(
        self, async_client: AsyncClient, create_configuration
    ):
        response = await async_client.put(
            self.url.format(configuration_id=create_configuration.id),
            json={
                "key": "test2",
                "type": "test",
            },
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    @pytest.mark.asyncio
    async def test_update_configuration_not_valid(
        self, async_client: AsyncClient, create_configuration
    ):
        response = await async_client.put(
            self.url.format(configuration_id=create_configuration.id),
            json={
                "key": "test2",
                "type": ConfigurationType.NUMBER.value,
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestConfigurationDelete:
    url = "/api/properties/settings/{configuration_id}"

    @pytest.mark.asyncio
    async def test_delete_configuration_success(
        self, async_client: AsyncClient, create_configuration
    ):
        response = await async_client.delete(
            self.url.format(configuration_id=create_configuration.id),
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = await async_client.get(
            self.url.format(configuration_id=create_configuration.id),
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_delete_configuration_not_found(self, async_client: AsyncClient):
        response = await async_client.delete(
            self.url.format(configuration_id=uuid4()),
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
