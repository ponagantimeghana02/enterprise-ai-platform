import { Box, Grid, Alert, CircularProgress } from "@mui/material";
import { useEffect, useState } from "react";

import SearchBar from "../../components/knowledge/SearchBar";
import FilterPanel from "../../components/knowledge/FilterPanel";
import UploadArea from "../../components/knowledge/UploadArea";
import DocumentTable from "../../components/knowledge/DocumentTable";

import { knowledgeService } from "../../services/knowledgeService";
import { Document } from "../../types/knowledge";

const KnowledgeBase = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    loadDocuments();
  }, []);

  async function loadDocuments() {
    try {
      setLoading(true);
      setError("");

      const response = await knowledgeService.getDocuments();
      setDocuments(response.documents);
    } catch (err) {
      console.error(err);
      setError("Failed to load documents.");
    } finally {
      setLoading(false);
    }
  }

  async function upload(file: File) {
    try {
      await knowledgeService.uploadDocument(file);
      loadDocuments();
    } catch (err) {
      console.error(err);
      setError("Failed to upload document.");
    }
  }

  async function deleteDocument(id: string) {
    try {
      await knowledgeService.deleteDocument(id);
      loadDocuments();
    } catch (err) {
      console.error(err);
      setError("Failed to delete document.");
    }
  }

  const filteredDocuments = documents.filter((doc) => {
    const matchesSearch = doc.name
      .toLowerCase()
      .includes(search.toLowerCase());

    const matchesStatus =
      status === "" || doc.status === status;

    return matchesSearch && matchesStatus;
  });

  return (
    <Box p={4}>
      <Grid container spacing={3}>

        {/* Upload */}
        <Grid item xs={12}>
          <UploadArea onUpload={upload} />
        </Grid>

        {/* Search */}
        <Grid item xs={12} md={8}>
          <SearchBar
            value={search}
            onChange={setSearch}
          />
        </Grid>

        {/* Filter */}
        <Grid item xs={12} md={4}>
          <FilterPanel
            status={status}
            onChange={setStatus}
          />
        </Grid>

        {/* Error Message */}
        {error && (
          <Grid item xs={12}>
            <Alert severity="error">
              {error}
            </Alert>
          </Grid>
        )}

        {/* Loading */}
        {loading ? (
          <Grid item xs={12}>
            <Box textAlign="center" py={4}>
              <CircularProgress />
            </Box>
          </Grid>
        ) : (
          <Grid item xs={12}>
            <DocumentTable
              documents={filteredDocuments}
              onDelete={deleteDocument}
            />
          </Grid>
        )}

      </Grid>
    </Box>
  );
};

export default KnowledgeBase;