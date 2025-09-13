"""
File storage utilities for handling file uploads and deletions.
This module provides functions to save and delete files on the server.
"""
import os
import uuid
from pathlib import Path
from typing import Optional, Union, BinaryIO

from fastapi import UploadFile, HTTPException, status

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

def get_upload_dir() -> Path:
    """
    Get the base upload directory.
    Creates the directory if it doesn't exist.
    
    Returns:
        Path: Path object pointing to the upload directory
    """
    upload_dir = Path(settings.UPLOAD_DIR) if hasattr(settings, 'UPLOAD_DIR') else Path("uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir

async def save_uploaded_file(
    file: Union[UploadFile, BinaryIO],
    subfolder: str = "",
    filename: Optional[str] = None,
    allowed_extensions: Optional[list] = None,
    max_size: int = 10 * 1024 * 1024  # 10MB default
) -> str:
    """
    Save an uploaded file to the server.
    
    Args:
        file: The uploaded file (FastAPI UploadFile or file-like object)
        subfolder: Subfolder within the upload directory
        filename: Custom filename (without extension). If None, a UUID will be used.
        allowed_extensions: List of allowed file extensions (e.g., ['.pdf', '.jpg'])
        max_size: Maximum file size in bytes
        
    Returns:
        str: Relative path to the saved file
        
    Raises:
        HTTPException: If file validation fails
    """
    try:
        # Get file info
        if hasattr(file, 'filename'):  # It's an UploadFile
            original_filename = file.filename
            content = await file.read()
        else:  # It's a file-like object
            original_filename = getattr(file, 'name', 'file')
            content = file.read()
        
        # Validate file size
        if len(content) > max_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds maximum allowed size of {max_size} bytes"
            )
        
        # Get file extension
        file_extension = Path(original_filename).suffix.lower()
        
        # Validate file extension
        if allowed_extensions and file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
            )
        
        # Generate a unique filename if not provided
        if not filename:
            filename = f"{uuid.uuid4().hex}{file_extension}"
        else:
            # Ensure the filename has the correct extension
            if not filename.lower().endswith(file_extension.lower()):
                filename = f"{filename}{file_extension}"
        
        # Create subfolder if it doesn't exist
        upload_dir = get_upload_dir() / subfolder
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Save the file
        file_path = upload_dir / filename
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Return the relative path
        relative_path = str(Path(subfolder) / filename) if subfolder else filename
        logger.info(f"File saved: {file_path}")
        return relative_path
        
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        if not isinstance(e, HTTPException):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save file"
            )
        raise

def delete_file(file_path: str) -> bool:
    """
    Delete a file from the server.
    
    Args:
        file_path: Relative path to the file (as returned by save_uploaded_file)
        
    Returns:
        bool: True if the file was deleted, False if it didn't exist
        
    Raises:
        HTTPException: If there's an error deleting the file
    """
    try:
        upload_dir = get_upload_dir()
        full_path = upload_dir / file_path
        
        # Check if file exists
        if not full_path.exists():
            return False
            
        # Delete the file
        full_path.unlink()
        logger.info(f"File deleted: {full_path}")
        
        # Try to remove parent directories if they're empty
        try:
            parent = full_path.parent
            while parent != upload_dir and not any(parent.iterdir()):
                parent.rmdir()
                parent = parent.parent
        except OSError:
            # Ignore errors when removing directories
            pass
            
        return True
        
    except Exception as e:
        logger.error(f"Error deleting file {file_path}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete file"
        )

def get_file_path(relative_path: str) -> Path:
    """
    Get the full filesystem path for a stored file.
    
    Args:
        relative_path: Relative path to the file (as returned by save_uploaded_file)
        
    Returns:
        Path: Full path to the file
        
    Raises:
        HTTPException: If the file doesn't exist or is outside the upload directory
    """
    try:
        upload_dir = get_upload_dir()
        full_path = (upload_dir / relative_path).resolve()
        
        # Security check: ensure the path is inside the upload directory
        if upload_dir.resolve() not in full_path.parents and full_path != upload_dir.resolve():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file path"
            )
            
        if not full_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
            )
            
        return full_path
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting file path: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error accessing file"
        )
