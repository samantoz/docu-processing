from pathlib import Path
from typing import List, Tuple


from paddleocr import PaddleOCR
from helper import visualize_ocr_result

class DocumentProcessor:
    """
    A class to handle document processing tasks including loading files,
    performing OCR, and extracting structured data.
    """

    def __init__(self, object_name: str = None):
        """
        Initialize the DocumentProcessor.

        Args:
            object_name (str, optional): The name of the file to process. Defaults to None.
        """
        self.object_name = object_name
        # Initialize the OCR model
        self.ocr_model = PaddleOCR(lang="en")
        self.document_path = self.load_object(object_name)

    def load_object(self, object_name: str):
        """
        Resolves the full path of the document object based on its extension.

        Args:
            object_name (str): The name of the file (e.g., 'document.pdf', 'image.png').

        Returns:
            str: The absolute path to the document if found, otherwise returns the resolved path string.
                 Returns None if object_name is None.
        """
        if object_name is None:
            return None

        print(f"Loading Document / Image {object_name}")
        
        # Determine directory based on file extension
        if object_name.endswith(".pdf"):
            obj_dir = Path("data/docs")
        else:
            # Default to images directory for non-pdf files
            obj_dir = Path("data/imgs")
        object_path = obj_dir / object_name
        
        # Verify file existence
        if not object_path.exists():
            print(f"File not found at {object_path.absolute()}")
            print(f"Current directory: {Path.cwd()}")
        return str(object_path)

    def process_document(self, document_path: str) -> List[Tuple[str, str]]:
        """
        Orchestrates the document processing pipeline: OCR followed by data extraction.

        Args:
            document_path (str): The file path of the document to process.

        Returns:
            List[Tuple[str, str]]: A list of key-value pairs extracted from the document.
        """
        print(f"Processing document: {document_path}")
        ocr_results = self.perform_ocr(document_path)
        structured_data = self.extract_structured_data(ocr_results)
        return structured_data

    def perform_ocr(self, document_path: str, visualize: bool = False, output_filename: str = None, show_in_vscode: bool = False) -> List[str]:
        """
        Simulates performing Optical Character Recognition (OCR) on a document.

        Args:
            document_path (str): The path to the document image or PDF.
            visualize (bool): Whether to visualize the OCR results.
            output_filename (str, optional): Filename to save visualization.
            show_in_vscode (bool): Whether to open the saved visualization in VS Code.

        Returns:
            List[str]: The extracted text lines from the OCR process.
        """
        print(f"Performing OCR on {document_path} using model {self.ocr_model}")
        # Run OCR using the standard ocr method
        result = self.ocr_model.predict(document_path)

        if not result or result[0] is None:
            return []
        page = result[0]
        texts = page['rec_texts']      # recognized text strings
        scores = page['rec_scores']    # confidence scores
        boxes = page['rec_polys']      # bounding box coordinates

        print(f"Extracted {len(texts)} text regions")
        print("\nFirst 10 regions:")
        for text, score, box in list(zip(texts, scores, boxes))[:10]:
            coords = box.astype(int).tolist()
            print(f"{text:40} | {score:.3f} | {coords}")

        if visualize:
            processed_img = page['doc_preprocessor_res']['output_img']
            visualize_ocr_result(processed_img, texts, boxes, output_filename=output_filename, show_in_vscode=show_in_vscode)

        return texts

    def extract_structured_data(self, ocr_results: List[str]) -> List[Tuple[str, str]]:
        """
        Extracts structured information from raw OCR results.

        Args:
            ocr_results (List[str]): The list of extracted text strings from the OCR step.

        Returns:
            List[Tuple[str, str]]: Extracted fields and their values.
        """
        print("Extracting structured data from OCR results")
        return [("Field1", "Value1"), ("Field2", "Value2")]

if __name__ == "__main__":
    
    # document_name = "dummy_statement.pdf"
    document_name = "receipt.jpg"
    output_filename = "ocr_" + document_name.replace(".", "_") + ".png"

    processor = DocumentProcessor(document_name)
    # print(f"Document path: {processor.document_path}")
    # structured_data = processor.process_document(processor.document_path)
    ocr_results = processor.perform_ocr(processor.document_path, visualize=True, output_filename=output_filename, show_in_vscode=True)
    
    # for field, value in structured_data:
        # print(f"{field}: {value}")