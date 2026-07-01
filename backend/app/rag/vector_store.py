"""
app/rag/vector_store.py
───────────────────────
Adapts database deletion hooks to use Cognee's dataset management APIs.
Keeps cleanups encapsulated so service files don't need to import Cognee directly.
"""

import asyncio
import logging
import cognee

logger = logging.getLogger(__name__)


async def delete_report_documents_async(patient_id: int, report_id: int) -> None:
    """
    Remove specific report data within the patient's dataset.
    """
    try:
        dataset_name = f"patient_{patient_id}"
        # We delete data associated with the report_id (which maps to the data_id in Cognee)
        # Using string matching since Cognee internally tracks files by name or UUID.
        # For simplicity, we can also empty the dataset and re-index active reports if needed,
        # but here we attempt to delete the specific data file:
        await cognee.datasets.delete_data(
            dataset_id=dataset_name,
            data_id=str(report_id)
        )
        logger.info("Cognee: Deleted data item '%d' from dataset '%s'", report_id, dataset_name)
    except Exception as e:
        logger.error("Cognee: Failed to delete data item %d: %s", report_id, e)


def delete_report_documents(patient_id: int, report_id: int) -> None:
    """Synchronous wrapper for delete_report_documents."""
    asyncio.run(delete_report_documents_async(patient_id, report_id))


async def delete_patient_collection_async(patient_id: int) -> None:
    """
    Delete the entire patient dataset (vector records, graph entities, etc.)
    when a patient record is removed from the system.
    """
    try:
        dataset_name = f"patient_{patient_id}"
        await cognee.datasets.empty_dataset(dataset_id=dataset_name)
        logger.info("Cognee: Emptied dataset '%s' for deleted patient", dataset_name)
    except Exception as e:
        logger.error("Cognee: Failed to empty dataset '%s': %s", dataset_name, e)


def delete_patient_collection(patient_id: int) -> None:
    """Synchronous wrapper for delete_patient_collection."""
    asyncio.run(delete_patient_collection_async(patient_id))
