import { useState } from "react";

import {
  Chip,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
} from "@mui/material";

import { Document } from "../../types/knowledge";

import StatusChip from "./StatusChip";
import DocumentActions from "./DocumentActions";
import PreviewDialog from "./PreviewDialog";

interface Props {
  documents: Document[];
  onDelete: (id: string) => void;
}

const DocumentTable = ({
  documents,
  onDelete,
}: Props) => {
  const [open, setOpen] = useState(false);

  const [selected, setSelected] =
    useState<Document | null>(null);

  const [page, setPage] = useState(0);

  const [rowsPerPage, setRowsPerPage] =
    useState(5);

  function preview(document: Document) {
    setSelected(document);
    setOpen(true);
  }

  function download(document: Document) {
    window.open(
      `/api/knowledge/${document.id}/download`,
      "_blank"
    );
  }

  return (
    <>
      <TableContainer component={Paper}>
        <Table>

          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>

              <TableCell>Type</TableCell>

              <TableCell>Tags</TableCell>

              <TableCell>Status</TableCell>

              <TableCell>Version</TableCell>

              <TableCell>Uploaded By</TableCell>

              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>

          <TableBody>
            {documents
              .slice(
                page * rowsPerPage,
                page * rowsPerPage +
                  rowsPerPage
              )
              .map((doc) => (
                <TableRow key={doc.id}>
                  <TableCell>
                    {doc.name}
                  </TableCell>

                  <TableCell>
                    {doc.type}
                  </TableCell>

                  <TableCell>
                    {doc.tags.map((tag) => (
                      <Chip
                        key={tag}
                        label={tag}
                        size="small"
                        sx={{ mr: 0.5, mb: 0.5 }}
                      />
                    ))}
                  </TableCell>

                  <TableCell>
                    <StatusChip
                      status={doc.status}
                    />
                  </TableCell>

                  <TableCell>
                    v1.0
                  </TableCell>

                  <TableCell>
                    {doc.uploadedBy}
                  </TableCell>

                  <TableCell>
                    <DocumentActions
                      onPreview={() =>
                        preview(doc)
                      }
                      onDownload={() =>
                        download(doc)
                      }
                      onDelete={() =>
                        onDelete(doc.id)
                      }
                    />
                  </TableCell>
                </TableRow>
              ))}
          </TableBody>

        </Table>

        <TablePagination
          component="div"
          count={documents.length}
          page={page}
          rowsPerPage={rowsPerPage}
          rowsPerPageOptions={[
            5,
            10,
            20,
          ]}
          onPageChange={(
            _,
            newPage
          ) => setPage(newPage)}
          onRowsPerPageChange={(e) => {
            setRowsPerPage(
              Number(e.target.value)
            );
            setPage(0);
          }}
        />
      </TableContainer>

      <PreviewDialog
        open={open}
        title={selected?.name || ""}
        content={
          selected
            ? `Preview of ${selected.name}`
            : ""
        }
        onClose={() => setOpen(false)}
      />
    </>
  );
};

export default DocumentTable;