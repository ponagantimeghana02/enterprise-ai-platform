export interface Document {
  id: string;
  name: string;
  type: string;
  size: number;
  uploadedBy: string;
  uploadedAt: string;
  status: "Pending" | "Approved" | "Rejected";
  tags: string[];
}

export interface KnowledgeResponse {
  documents: Document[];
}