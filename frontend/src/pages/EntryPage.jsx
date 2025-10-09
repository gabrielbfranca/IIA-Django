import { Link } from "react-router-dom";
import React from "react";
import "../assets/styles/styles.css";
import {
  CButton,
  CCard,
  CCardBody,
  CCardFooter,
  CCardHeader,
  CCardText,
  CCardTitle,
} from "@coreui/react";

const EntryPage = () => {
  return (
    <div className="mainCard">
      <CCard className="text-center">
        <CCardHeader>Página Inicial</CCardHeader>
        <CCardBody>
          <CCardTitle>Bem vindo</CCardTitle>
          <CCardText>
            Com texto de apoio abaixo como uma introdução natural a conteúdo
            adicional.
          </CCardText>
          <div className="button-group">
            <CButton color="primary" href="/login">
              Login
            </CButton>
            <CButton color="secondary" href="/signup">
              Sign Up
            </CButton>
          </div>
        </CCardBody>
        <CCardFooter className="text-body-secondary">2 dias atrás</CCardFooter>
      </CCard>
    </div>
  );
};
export default EntryPage;
