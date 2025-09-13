# Project Directory Tree

This document provides a visual representation of the project's file structure.

```
sila-system/
├── .bandit.yml
├── .env
├── .env.example
├── .flake8
├── .gitattributes
├── .github/
│   └── workflows/
│       ├── backend-tests.yml
│       ├── ci-validation.yml
│       ├── ci.yml
│       └── database-migrations.yml
├── .markdownlint.json
├── .pre-commit-config.yaml
├── .pytest_cache/
│   ├── CACHEDIR.TAG
│   └── v/
│       └── cache/
│           ├── lastfailed
│           └── nodeids
├── .windsurfignore
├── analyze_issues.py
├── aplicar_correcoes.bat
├── ARQUITETURA.md
├── backend/
│   ├── .github/
│   │   └── workflows/
│   │       └── tests.yml
│   ├── .nodeenv/
│   │   ├── Scripts/
│   │   │   ├── activate.bat
│   │   │   ├── corepack
│   │   │   ├── corepack.cmd
│   │   │   ├── install_tools.bat
│   │   │   ├── nodevars.bat
│   │   │   ├── npm
│   │   │   ├── npm.cmd
│   │   │   ├── npx
│   │   │   └── npx.cmd
│   │   └── src/
│   │       └── node-v20.12.2-win-x64/
│   │           ├── corepack
│   │           ├── corepack.cmd
│   │           ├── install_tools.bat
│   │           ├── nodevars.bat
│   │           ├── npm
│   │           ├── npm.cmd
│   │           ├── npx
│   │           └── npx.cmd
│   ├── 0.1.4
│   ├── alembic/
│   │   ├── env.py
│   │   ├── README
│   │   ├── script.py.mako
│   │   └── versions/
│   │       ├── db385a402cb9_initial_models.py
│   │       ├── db385a402cb9_initial_models.py.bak
│   │       └── db385a402cb9_initial_models.py.bak2
│   ├── alembic.ini
│   ├── alembic_upgrade_log.txt
│   ├── API_TESTING_SETUP.md
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── deps.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── api.py
│   │   │       └── endpoints/
│   │   │           ├── auth.py
│   │   │           └── users.py
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   └── security.py
│   │   ├── auth_utils.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── application.py
│   │   │   ├── approval_decorator.py
│   │   │   ├── auth/
│   │   │   │   ├── auth.py
│   │   │   │   ├── auth_utils.py
│   │   │   │   ├── enhanced_auth.py
│   │   │   │   ├── permissions.py
│   │   │   │   └── security.py
│   │   │   ├── business_rules.py
│   │   │   ├── cache.py
│   │   │   ├── config/
│   │   │   │   ├── __init__.py
│   │   │   │   └── settings.py
│   │   │   ├── config.py
│   │   │   ├── db/
│   │   │   │   └── __init__.py
│   │   │   ├── exceptions.py
│   │   │   ├── i18n/
│   │   │   │   └── i18n.py
│   │   │   ├── logging/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── logging_config.py
│   │   │   │   ├── metrics.py
│   │   │   │   ├── metrics_manager.py
│   │   │   │   ├── observability_middleware.py
│   │   │   │   ├── prometheus_metrics.py
│   │   │   │   └── structured_logging.py
│   │   │   ├── logging.py
│   │   │   ├── middleware/
│   │   │   │   └── __init__.py
│   │   │   ├── responses.py
│   │   │   ├── scheduler.py
│   │   │   ├── security.py
│   │   │   ├── versioning.py
│   │   │   └── workflow.py
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── base_class.py
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   └── user.py
│   │   │   ├── repositories/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py
│   │   │   │   └── user.py
│   │   │   └── session.py
│   │   ├── main.py
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   ├── audit_log.py
│   │   │   ├── audit_middleware.py
│   │   │   └── error_handler.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── address_geocodificacao_endereco.py
│   │   │   ├── address_normalizacao_endereco.py
│   │   │   ├── address_validacao_c_e_p.py
│   │   │   ├── auth_autenticacao_multifator.py
│   │   │   ├── auth_controle_acesso.py
│   │   │   ├── auth_gestao_usuario.py
│   │   │   ├── auth_sessao_segura.py
│   │   │   ├── citizenship_atualizacao_b_i.py
│   │   │   ├── citizenship_atualizacao_endereco.py
│   │   │   ├── citizenship_certidao_casamento.py
│   │   │   ├── citizenship_certidao_nascimento.py
│   │   │   ├── citizenship_certidao_obito.py
│   │   │   ├── citizenship_declaracao_residencia.py
│   │   │   ├── citizenship_emissao_b_i.py
│   │   │   ├── citizenship_emissao_passaporte.py
│   │   │   ├── citizenship_regitro_eleitoral.py
│   │   │   ├── citizenship_visto_permanencia.py
│   │   │   ├── commercial_abertura_processo.py
│   │   │   ├── commercial_alvara_comercial.py
│   │   │   ├── commercial_certificacao_origem.py
│   │   │   ├── commercial_contrato_publico.py
│   │   │   ├── commercial_fiscalizacao_mercado.py
│   │   │   ├── commercial_inspecao_sanitaria.py
│   │   │   ├── commercial_licenca_importacao.py
│   │   │   ├── commercial_licenca_industrial.py
│   │   │   ├── commercial_registo_empresa.py
│   │   │   ├── commercial_registo_marca.py
│   │   │   ├── commercial_taxa_comercial.py
│   │   │   ├── common_cache_distribuido.py
│   │   │   ├── common_configuracao_global.py
│   │   │   ├── common_log_sistema.py
│   │   │   ├── common_validador_formulario.py
│   │   │   ├── documents_assinatura_digital.py
│   │   │   ├── documents_gerador_documento.py
│   │   │   ├── documents_template_documento.py
│   │   │   ├── education_alfabetizacao_adulto.py
│   │   │   ├── education_bolsa_estudo.py
│   │   │   ├── education_curso_tecnico.py
│   │   │   ├── education_educacao_especial.py
│   │   │   ├── education_ensino_superior.py
│   │   │   ├── education_historico_escolar.py
│   │   │   ├── education_matricula_escolar.py
│   │   │   ├── education_merenda_escolar.py
│   │   │   ├── education_transferencia_escolar.py
│   │   │   ├── education_transporte_escolar.py
│   │   │   ├── finance_apoio_empreendedor.py
│   │   │   ├── finance_consulta_debito.py
│   │   │   ├── finance_contabilidade_publica.py
│   │   │   ├── finance_declaracao_impostos.py
│   │   │   ├── finance_emissao_recibo.py
│   │   │   ├── finance_isencao_taxa.py
│   │   │   ├── finance_micro_credito.py
│   │   │   ├── finance_pagamento_taxa.py
│   │   │   ├── finance_parcelamento_debito.py
│   │   │   ├── finance_payment.py
│   │   │   ├── finance_subsidio_habitacao.py
│   │   │   ├── finance_transaction.py
│   │   │   ├── governance_audit_log.py
│   │   │   ├── governance_auditoria_log.py
│   │   │   ├── governance_controle_versao.py
│   │   │   ├── governance_gestao_risco.py
│   │   │   ├── governance_politica_seguranca.py
│   │   │   ├── health_agendamento_consulta.py
│   │   │   ├── health_agendamento_teleconsulta.py
│   │   │   ├── health_agendamento_vacinacao.py
│   │   │   ├── health_avaliacao_nutricional.py
│   │   │   ├── health_cartao_vacina.py
│   │   │   ├── health_consulta_telematica.py
│   │   │   ├── health_emergencia_medica.py
│   │   │   ├── health_historico_medico.py
│   │   │   ├── health_seguro_saude.py
│   │   │   ├── health_solicitacao_exame.py
│   │   │   ├── health_solicitacao_medicamento.py
│   │   │   ├── integration_a_p_i_gateway.py
│   │   │   ├── integration_conector_externo.py
│   │   │   ├── integration_integration_event.py
│   │   │   ├── integration_sincronizacao_b_n_a.py
│   │   │   ├── integration_transformacao_dados.py
│   │   │   ├── internal_manutencao_preventiva.py
│   │   │   ├── internal_monitoramento_sistema.py
│   │   │   ├── internal_otimizacao_performance.py
│   │   │   ├── justice_assistencia_juridica.py
│   │   │   ├── justice_defensor_publico.py
│   │   │   ├── justice_execucao_fiscal.py
│   │   │   ├── justice_habeas_corpus.py
│   │   │   ├── justice_leilao_judicial.py
│   │   │   ├── justice_mandado_seguranca.py
│   │   │   ├── justice_mediacao_conflito.py
│   │   │   ├── justice_penhonha_bens.py
│   │   │   ├── justice_registo_criminal.py
│   │   │   ├── registry_adocao_menor.py
│   │   │   ├── registry_certidao_negativa.py
│   │   │   ├── registry_citizen.py
│   │   │   ├── registry_reconhecimento_paternidade.py
│   │   │   ├── registry_registo_casamento.py
│   │   │   ├── registry_registo_civil.py
│   │   │   ├── registry_registo_imovel.py
│   │   │   ├── registry_registo_nascimento.py
│   │   │   ├── registry_registo_obito.py
│   │   │   ├── registry_retificacao_registro.py
│   │   │   ├── registry_tutela_menor.py
│   │   │   ├── sanitation_agente_sanitario.py
│   │   │   ├── sanitation_controle_vetores.py
│   │   │   ├── sanitation_educacao_ambiental.py
│   │   │   ├── sanitation_esgoto_sanitario.py
│   │   │   ├── sanitation_limpeza_urbana.py
│   │   │   ├── sanitation_monitoramento_ambiental.py
│   │   │   ├── sanitation_tratamento_agua.py
│   │   │   ├── social_assistencia_mulher.py
│   │   │   ├── social_auxilio_social.py
│   │   │   ├── social_bolsa_familia.py
│   │   │   ├── social_capacitacao_profissional.py
│   │   │   ├── social_habitacao_social.py
│   │   │   ├── social_inclusao_digital.py
│   │   │   ├── social_programa_idoso.py
│   │   │   ├── social_protecao_menor.py
│   │   │   ├── social_reabilitacao_social.py
│   │   │   ├── social_seguranca_alimentar.py
│   │   │   ├── statistics_analise_dados.py
│   │   │   ├── statistics_dashboard_executivo.py
│   │   │   ├── statistics_metricas_uso.py
│   │   │   ├── statistics_relatorio_k_p_i.py
│   │   │   ├── urbanism_alvara_funcionamento.py
│   │   │   ├── urbanism_demolicao_edificio.py
│   │   │   ├── urbanism_espaco_publico.py
│   │   │   ├── urbanism_inspecao_obra.py
│   │   │   ├── urbanism_licenca_construcao.py
│   │   │   ├── urbanism_loteamento_urbano.py
│   │   │   ├── urbanism_ocupacao_solo.py
│   │   │   ├── urbanism_plano_urbano.py
│   │   │   ├── urbanism_regularizacao_fundiaria.py
│   │   │   └── urbanism_sinalizacao_trafego.py
│   │   ├── modules/
│   │   │   ├── __init__.py
│   │   │   ├── address/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── geocodificacao_endereco.py
│   │   │   │   │   ├── normalizacao_endereco.py
│   │   │   │   │   └── validacao_c_e_p.py
│   │   │   │   ├── routes/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── geocodificacao_endereco.py
│   │   │   │   │   ├── normalizacao_endereco.py
│   │   │   │   │   └── validacao_c_e_p.py
│   │   │   │   ├── schemas/
│   │   │   │   │   ├── geocodificacao_endereco.py
│   │   │   │   │   ├── normalizacao_endereco.py
│   │   │   │   │   └── validacao_c_e_p.py
│   │   │   │   ├── services/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── address_service.py
│   │   │   │   └── tests/
│   │   │   │       └── __init__.py
│   │   │   ├── appointments/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models/
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── routes/
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── services/
│   │   │   │   │   └── __init__.py
│   │   │   │   └── tests/
│   │   │   │       └── __init__.py
│   │   │   ├── auth/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models/
│   │   │   │   │   ├── autenticacao_multifator.py
│   │   │   │   │   ├── controle_acesso.py
│   │   │   │   │   ├── gestao_usuario.py
│   │   │   │   │   └── sessao_segura.py
│   │   │   │   └── routes/
│   │   │   │       ├── autenticacao_multifator.py
│   │   │   │       ├── controle_acesso.py
│   │   │   │       ├── gestao_usuario.py
│   │   │   │       └── sessao_segura.py
│   │   │   ├── citizenship/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── atualizacao_b_i.py
│   │   │   │   │   ├── atualizacao_endereco.py
│   │   │   │   │   ├── certidao_casamento.py
│   │   │   │   │   ├── certidao_nascimento.py
│   │   │   │   │   ├── certidao_obito.py
│   │   │   │   │   ├── declaracao_residencia.py
│   │   │   │   │   ├── emissao_b_i.py
│   │   │   │   │   ├── emissao_passaporte.py
│   │   │   │   │   ├── regitro_eleitoral.py
│   │   │   │   │   └── visto_permanencia.py
│   │   │   │   ├── routes/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── atualizacao_b_i.py
│   │   │   │   │   ├── atualizacao_endereco.py
│   │   │   │   │   ├── certidao_casamento.py
│   │   │   │   │   ├── certidao_nascimento.py
│   │   │   │   │   ├── certidao_obito.py
│   │   │   │   │   ├── declaracao_residencia.py
│   │   │   │   │   ├── emissao_b_i.py
│   │   │   │   │   ├── emissao_bi_route.py
│   │   │   │   │   ├── emissao_passaporte.py
│   │   │   │   │   ├── regitro_eleitoral.py
│   │   │   │   │   └── visto_permanencia.py
│   │   │   │   ├── services/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── event_handlers.py
│   │   │   │   ├── tests/
│   │   │   │   │   └── __init__.py
│   │   │   │   └── utils/
│   │   │   │       ├── __init__.py
│   │   │   │       ├── permission_checker.py
│   │   │   │       └── route_analyzer.py
│   │   │   ├── commercial/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── abertura_processo.py
│   │   │   │   │   ├── alvara_comercial.py
│   │   │   │   │   ├── certificacao_origem.py
│   │   │   │   │   ├── contrato_publico.py
│   │   │   │   │   ├── fiscalizacao_mercado.py
│   │   │   │   │   ├── inspecao_sanitaria.py
│   │   │   │   │   ├── licenca_importacao.py
│   │   │   │   │   ├── licenca_industrial.py
│   │   │   │   │   ├── registo_empresa.py
│   │   │   │   │   ├── registo_marca.py
│   │   │   │   │   └── taxa_comercial.py
│   │   │   │   ├── routes/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── abertura_processo.py
│   │   │   │   │   ├── alvara_comercial.py
│   │   │   │   │   ├── certificacao_origem.py
│   │   │   │   │   ├── contrato_publico.py
│   │   │   │   │   ├── fiscalizacao_mercado.py
│   │   │   │   │   ├── inspecao_sanitaria.py
│   │   │   │   │   ├── licenca_importacao.py
│   │   │   │   │   ├── licenca_industrial.py
│   │   │   │   │   ├── registo_empresa.py
│   │   │   │   │   ├── registo_marca.py
│   │   │   │   │   └── taxa_comercial.py
│   │   │   │   ├── services/
│   │   │   │   │   └── __init__.py
│   │   │   │   └── tests/
│   │   │   │       └── __init__.py
│   │   │   ├── common/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── cache_distribuido.py
│   │   │   │   │   ├── configuracao_global.py
│   │   │   │   │   ├── log_sistema.py
│   │   │   │   │   └── validador_formulario.py
│   │   │   │   ├── routes/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── cache_distribuido.py
│   │   │   │   │   ├── configuracao_global.py
│   │   │   │   │   ├── log_sistema.py
│   │   │   │   │   └── validador_formulario.py
│   │   │   │   ├── services/
│   │   │   │   │   └── __init__.py
│   │   │   │   └── tests/
│   │   │   │       └── __init__.py
│   │   │   ├── complaints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── routes/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── corrupcao_administrativa.py
│   │   │   │   │   ├── denuncia_ambiental.py
│   │   │   │   │   ├── denuncia_cidada.py
│   │   │   │   │   ├── fiscalizacao_obra.py
│   │   │   │   │   ├── irregularidade_fiscal.py
│   │   │   │   │   ├── mau_atendimento.py
│   │   │   │   │   ├── ouvidoria_municipal.py
│   │   │   │   │   ├── reclamacao_servico.py
│   │   │   │   │   ├── sugestao_melhoria.py
│   │   │   │   │   └── violacao_direitos.py
│   │   │   │   └── tests/
│   │   │   │       ├── __init__.py
│   │   │   │       └── conftest.py
│   │   │   ├── documents/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── assinatura_digital.py
│   │   │   │   │   ├── gerador_documento.py
│   │   │   │   │   └── template_documento.py
│   │   │   │   ├── routes/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── assinatura_digital.py
│   │   │   │   │   ├── gerador_documento.py
│   │   │   │   │   └── template_documento.py
│   │   │   │   ├── schemas/
│   │   │   │   │   ├── assinatura_digital.py
│   │   │   │   │   ├── gerador_documento.py
│   │   │   │   │   └── template_documento.py
│   │   │   │   ├── services/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── document_service.py
│   │   │   │   └── tests/
│   │   │   │       └── __init__.py
│   │   │   ├── education/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── alfabetizacao_adulto.py
│   │   │   │   │   ├── bolsa_estudo.py
│   │   │   │   │   ├── curso_tecnico.py
│   │   │   │   │   ├── educacao_especial.py
│   │   │   │   │   ├── ensino_superior.py
│   │   │   │   │   ├── historico_escolar.py
│   │   │   │   │   ├── matricula_escolar.py
│   │   │   │   │   ├── merenda_escolar.py
│   │   │   │   │   ├── transferencia_escolar.py
│   │   │   │   │   └── transporte_escolar.py
│   │   │   │   ├── routes/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── alfabetizacao_adulto.py
│   │   │   │   │   ├── bolsa_estudo.py
│   │   │   │   │   ├── curso_tecnico.py
│   │   │   │   │   ├── educacao_especial.py
│   │   │   │   │   ├── ensino_superior.py
│   │   │   │   │   ├── historico_escolar.py
│   │   │   │   │   ├── matricula_escolar.py
│   │   │   │   │   ├── merenda_escolar.py
│   │   │   │   │   ├── transferencia_escolar.py
│   │   │   │   │   └── transporte_escolar.py
│   │   │   │   ├── services/
│   │   │   │   │   └── __init__.py
│   │   │   │   └── tests/
│   │   │   │       └── __init__.py
│   │   │   ├── finance/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── apoio_empreendedor.py
│   │   │   │   │   ├── consulta_debito.py
│   │   │   │   │   ├── contabilidade_publica.py
│   │   │   │   │   ├── declaracao_impostos.py
│   │   │   │   │   ├── emissao_recibo.py
│   │   │   │   │   ├── isencao_taxa.py
│   │   │   │   │   ├── micro_credito.py
│   │   │   │   │   ├── pagamento_taxa.py
│   │   │   │   │   ├── parcelamento_debito.py
│   │   │   │   │   ├── payment.py
│   │   │   │   │   ├── subsidio_habitacao.py
│   │   │   │   │   └── transaction.py
│   │   │   │   ├── routes/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── apoio_empreendedor.py
│   │   │   │   │   ├── consulta_debito.py
│   │   │   │   │   ├── contabilidade_publica.py
│   │   │   │   │   ├── declaracao_impostos.py
│   │   │   │   │   ├── emissao_recibo.py
│   │   │   │   │   ├── isencao_taxa.py
│   │   │   │   │   ├── micro_credito.py
│   │   │   │   │   ├── pagamento_taxa.py
│   │   │   │   │   ├── parcelamento_debito.py
│   │   │   │   │   └── subsidio_habitacao.py
│   │   │   │   ├── schemas/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── apoio_empreendedor.py
│   │   │   │   │   ├── consulta_debito.py
│   │   │   │   │   ├── contabilidade_publica.py
│   │   │   │   │   ├── declaracao_impostos.py
│   │   │   │   │   ├── emissao_recibo.py
│   │   │   │   │   ├── isencao_taxa.py
│   │   │   │   │   ├── micro_credito.py
│   │   │   │   │   ├── pagamento_taxa.py
│   │   │   │   │   ├── parcelamento_debito.py
│   │   │   │   │   └── subsidio_habitacao.py
│   │   │   │   ├── services/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── payment.py
│   │   │   │   ├── tests/
│   │   │   │   │   └── __init__.py
│   │   │   │   └── utils/
│   │   │   │       └── __init__.py
│   │   │   ├── governance/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── audit_log.py
│   │   │   │   │   ├── auditoria_log.py
│   │   │   │   │   ├── controle_versao.py
│   │   │   │   │   ├── gestao_risco.py
│   │   │   │   │   └── politica_seguranca.py
│   │   │   │   ├── routes/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── auditoria_log.py
│   │   │   │   │   ├── controle_versao.py
│   │   │   │   │   ├── gestao_risco.py
│   │   │   │   │   └── politica_seguranca.py
│   │   │   │   ├── schemas/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── auditoria_log.py
│   │   │   │   │   ├── controle_versao.py
│   │   │   │   │   ├── gestao_risco.py
│   │   │   │   │   └── politica_seguranca.py
│   │   │   │   ├── services/
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── tests/
│   │   │   │   │   └── __init__.py
│   │   │   │   └── utils/
│   │   │   │       └── __init__.py
│   │   │   ├── health/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── health_services/
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── models/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── agendamento_consulta.py
│   │   │   │   │   ├── agendamento_teleconsulta.py
│   │   │   │   │   ├── agendamento_vacinacao.py
│   │   │   │   │   ├── avaliacao_nutricional.py
│   │   │   │   │   ├── cartao_vacina.py
│   │   │   │   │   ├── consulta_telematica.py
│   │   │   │   │   ├── emergencia_medica.py
│   │   │   │   │   ├── historico_medico.py
│   │   │   │   │   ├── seguro_saude.py
│   │   │   │   │   ├── solicitacao_exame.py
│   │   │   │   │   └── solicitacao_medicamento.py
│   │   │   │   ├── routes/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── agendamento_consulta.py
│   │   │   │   │   ├── agendamento_teleconsulta.py
│   │   │   │   │   ├── agendamento_vacinacao.py
│   │   │   │   │   ├── avaliacao_nutricional.py
│   │   │   │   │   ├── cartao_vacina.py
│   │   │   │   │   ├── consulta_telematica.py
│   │   │   │   │   ├── emergencia_medica.py
│   │   │   │   │   ├── historico_medico.py
│   │   │   │   │   ├── seguro_saude.py
│   │   │   │   │   ├── solicitacao_exame.py
│   │   │   │   │   └── solicitacao_medicamento.py
│   │   │   │   └── tests/
│   │   │   │       └── __init__.py
│   │   │   ├── identity/
│   │   │   │   └── __init__.py
│   │   │   ├── integration/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── adapters/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── bna_adapter.py
│   │   │   │   ├── examples/
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── models/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── a_p_i_gateway.py
│   │   │   │   │   ├── conector_externo.py
│   │   │   │   │   ├── integration_event.py
│   │   │   │   │   ├── sincronizacao_b_n_a.py
│   │   │   │   │   └── transformacao_dados.py
│   │   │   │   ├── routes/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── a_p_i_gateway.py
│   │   │   │   │   ├── conector_externo.py
│   │   │   │   │   ├── event_routes.py
│   │   │   │   │   ├── sincronizacao_b_n_a.py
│   │   │   │   │   └── transformacao_dados.py
│   │   │   │   ├── schemas/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── a_p_i_gateway.py
│   │   │   │   │   ├── conector_externo.py
│   │   │   │   │   ├── event_schemas.py
│   │   │   │   │   ├── sincronizacao_b_n_a.py
│   │   │   │   │   └── transformacao_dados.py
│   │   │   │   ├── services/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── event_service.py
│   │   │   │   ├── tests/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── test_integration_gateway.py
│   │   │   │   └── utils/
│   │   │   │       └── __init__.py
│   │   │   ├── internal/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── manutencao_preventiva.py
│   │   │   │   │   ├── monitoramento_sistema.py
│   │   │   │   │   └── otimizacao_performance.py
│   │   │   │   ├── routes/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── manutencao_preventiva.py
│   │   │   │   │   ├── monitoramento_sistema.py
│   │   │   │   │   └── otimizacao_performance.py
│   │   │   │   ├── services/
│   │   │   │   │   └── __init__.py
│   │   │   │   └── tests/
│   │   │   │       └── __init__.py
│   │   │   ├── journeys/
│   │   │   │   └── __init__.py
│   │   │   ├── justice/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── assistencia_juridica.py
│   │   │   │   │   ├── defensor_publico.py
│   │   │   │   │   ├── execucao_fiscal.py
│   │   │   │   │   ├── habeas_corpus.py
│   │   │   │   │   ├── leilao_judicial.py
│   │   │   │   │   ├── mandado_seguranca.py
│   │   │   │   │   ├── mediacao_conflito.py
│   │   │   │   │   ├── penhonha_bens.py
│   │   │   │   │   └── registo_criminal.py
│   │   │   │   ├── routes/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── assistencia_juridica.py
│   │   │   │   │   ├── defensor_publico.py
│   │   │   │   │   ├── execucao_fiscal.py
│   │   │   │   │   ├── habeas_corpus.py
│   │   │   │   │   ├── leilao_judicial.py
│   │   │   │   │   ├── mandado_seguranca.py
│   │   │   │   │   ├── mediacao_conflito.py
│   │   │   │   │   ├── penhonha_bens.py
│   │   │   │   │   └── registo_criminal.py
│   │   │   │   ├── services/
│   │   │   │   │   └── __init__.py
│   │   │   │   └── tests/
│   │   │   │       └── __init__.py
│   │   │   ├── location/
│   │   │   │   └── __init__.py
│   │   │   ├── monitoring/
│   │   │   │   ├── __init__.py
│   │   │   │   └── routes/
│   │   │   │       ├── health.py
│   │   │   │       ├── metrics.py
│   │   │   │       └── tracing.py
│   │   │   ├── notification/
│   │   │   │   └── __init__.py
│   │   │   ├── payment/
│   │   │   │   └── __init__.py
│   │   │   ├── registry/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── adocao_menor.py
│   │   │   │   │   ├── certidao_negativa.py
│   │   │   │   │   ├── citizen.py
│   │   │   │   │   ├── reconhecimento_paternidade.py
│   │   │   │   │   ├── registo_casamento.py
│   │   │   │   │   ├── registo_civil.py
│   │   │   │   │   ├── registo_imovel.py
│   │   │   │   │   ├── registo_nascimento.py
│   │   │   │   │   ├── registo_obito.py
│   │   │   │   │   ├── retificacao_registro.py
│   │   │   │   │   └── tutela_menor.py
│   │   │   │   ├── routes/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── adocao_menor.py
│   │   │   │   │   ├── certidao_negativa.py
│   │   │   │   │   ├── reconhecimento_paternidade.py
│   │   │   │   │   ├── registo_casamento.py
│   │   │   │   │   ├── registo_civil.py
│   │   │   │   │   ├── registo_imovel.py
│   │   │   │   │   ├── registo_nascimento.py
│   │   │   │   │   ├── registo_obito.py
│   │   │   │   │   ├── retificacao_registro.py
│   │   │   │   │   └── tutela_menor.py
│   │   │   │   ├── schemas/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── adocao_menor.py
│   │   │   │   │   ├── certidao_negativa.py
│   │   │   │   │   ├── reconhecimento_paternidade.py
│   │   │   │   │   ├── registo_casamento.py
│   │   │   │   │   ├── registo_civil.py
│   │   │   │   │   ├── registo_imovel.py
│   │   │   │   │   ├── registo_nascimento.py
│   │   │   │   │   ├── registo_obito.py
│   │   │   │   │   ├── retificacao_registro.py
│   │   │   │   │   └── tutela_menor.py
│   │   │   │   ├── services/
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── tests/
│   │   │   │   │   └── __init__.py
│   │   │   │   └── utils/
│   │   │   │       └── __init__.py
│   │   │   ├── reports/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models/
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── routes/
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── services/
│   │   │   │   │   └── __init__.py
│   │   │   │   └── tests/
│   │   │   │       └── __init__.py
│   │   │   ├── sanitation/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── agente_sanitario.py
│   │   │   │   │   ├── controle_vetores.py
│   │   │   │   │   ├── educacao_ambiental.py
│   │   │   │   │   ├── esgoto_sanitario.py
│   │   │   │   │   ├── limpeza_urbana.py
│   │   │   │   │   ├── monitoramento_ambiental.py
│   │   │   │   │   └── tratamento_agua.py
│   │   │   │   ├── routes/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── agente_sanitario.py
│   │   │   │   │   ├── controle_vetores.py
│   │   │   │   │   ├── educacao_ambiental.py
│   │   │   │   │   ├── esgoto_sanitario.py
│   │   │   │   │   ├── limpeza_urbana.py
│   │   │   │   │   ├── monitoramento_ambiental.py
│   │   │   │   │   └── tratamento_agua.py
│   │   │   │   ├── services/
│   │   │   │   │   └── __init__.py
│   │   │   │   └── tests/
│   │   │   │       └── __init__.py
│   │   │   ├── service_hub/
│   │   │   │   ├── __init__.py
│   │   │   │   └── tests/
│   │   │   │       ├── __init__.py
│   │   │   │       ├── test_endpoints.py
│   │   │   │       └── test_services.py
│   │   │   ├── social/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── assistencia_mulher.py
│   │   │   │   │   ├── auxilio_social.py
│   │   │   │   │   ├── bolsa_familia.py
│   │   │   │   │   ├── capacitacao_profissional.py
│   │   │   │   │   ├── habitacao_social.py
│   │   │   │   │   ├── inclusao_digital.py
│   │   │   │   │   ├── programa_idoso.py
│   │   │   │   │   ├── protecao_menor.py
│   │   │   │   │   ├── reabilitacao_social.py
│   │   │   │   │   └── seguranca_alimentar.py
│   │   │   │   ├── routes/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── assistencia_mulher.py
│   │   │   │   │   ├── auxilio_social.py
│   │   │   │   │   ├── bolsa_familia.py
│   │   │   │   │   ├── capacitacao_profissional.py
│   │   │   │   │   ├── habitacao_social.py
│   │   │   │   │   ├── inclusao_digital.py
│   │   │   │   │   ├── programa_idoso.py
│   │   │   │   │   ├── protecao_menor.py
│   │   │   │   │   ├── reabilitacao_social.py
│   │   │   │   │   └── seguranca_alimentar.py
│   │   │   │   ├── services/
│   │   │   │   │   └── __init__.py
│   │   │   │   └── tests/
│   │   │   │       └── __init__.py
│   │   │   ├── statistics/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── analise_dados.py
│   │   │   │   │   ├── dashboard_executivo.py
│   │   │   │   │   ├── metricas_uso.py
│   │   │   │   │   └── relatorio_k_p_i.py
│   │   │   │   ├── routes/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── analise_dados.py
│   │   │   │   │   ├── dashboard_executivo.py
│   │   │   │   │   ├── metricas_uso.py
│   │   │   │   │   └── relatorio_k_p_i.py
│   │   │   │   ├── services/
│   │   │   │   │   └── __init__.py
│   │   │   │   └── tests/
│   │   │   │       └── __init__.py
│   │   │   ├── training/
│   │   │   │   ├── __init__.py
│   │   │   │   └── routes/
│   │   │   │       └── training.py
│   │   │   └── urbanism/
│   │   │       ├── __init__.py
│   │   │       ├── models/
│   │   │       │   ├── __init__.py
│   │   │       │   ├── alvara_funcionamento.py
│   │   │       │   ├── demolicao_edificio.py
│   │   │       │   ├── espaco_publico.py
│   │   │       │   ├── inspecao_obra.py
│   │   │       │   ├── licenca_construcao.py
│   │   │       │   ├── loteamento_urbano.py
│   │   │       │   ├── ocupacao_solo.py
│   │   │       │   ├── plano_urbano.py
│   │   │       │   ├── regularizacao_fundiaria.py
│   │   │       │   └── sinalizacao_trafego.py
│   │   │       ├── routes/
│   │   │       │   ├── __init__.py
│   │   │       │   ├── alvara_funcionamento.py
│   │   │       │   ├── demolicao_edificio.py
│   │   │       │   ├── espaco_publico.py
│   │   │       │   ├── inspecao_obra.py
│   │   │       │   ├── licenca_construcao.py
│   │   │       │   ├── loteamento_urbano.py
│   │   │       │   ├── ocupacao_solo.py
│   │   │       │   ├── plano_urbano.py
│   │   │       │   ├── regularizacao_fundiaria.py
│   │   │       │   └── sinalizacao_trafego.py
│   │   │       ├── services/
│   │   │       │   └── __init__.py
│   │   │       └── tests/
│   │   │           └── __init__.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── services.py
│   │   │   ├── token.py
│   │   │   └── user.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── document_validation_metrics.py
│   │   │   ├── faturacao_api.py
│   │   │   ├── image_validator.py
│   │   │   ├── monitoring.py
│   │   │   ├── notificacoes.py
│   │   │   ├── notification_service.py
│   │   │   ├── permission_service.py
│   │   │   └── user_service.py
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── conftest.py
│   │   │   ├── integration/
│   │   │   │   └── __init__.py
│   │   │   └── unit/
│   │   │       └── __init__.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── file_upload.py
│   │       ├── geo_utils.py
│   │       ├── pdf_generator.py
│   │       └── validador_foto.py
│   ├── AUTOMATED_SERVICE_TESTING.md
│   ├── check_env.py
│   ├── check_postgres.py
│   ├── create_superuser.py
│   ├── create_user.py
│   ├── Dockerfile
│   ├── docs/
│   │   ├── authentication.md
│   │   ├── estado_atual_reestruturacao.md
│   │   ├── OBSERVABILITY.md
│   │   ├── README_onboarding.md
│   │   ├── STATE_REESTRUTURACAO.md
│   │   └── user-guide/
│   │       └── account-security.md
│   ├── env.example
│   ├── find_locking_process.ps1
│   ├── get-pip.py
│   ├── init_db.py
│   ├── integration/
│   │   └── adapters/
│   │       └── simplifica_adapter.py
│   ├── logs/
│   ├── main.py
│   ├── module_health_dashboard.html
│   ├── modules_services.json
│   ├── observability/
│   │   ├── __init__.py
│   │   └── sentry_config.py
│   ├── organize.ps1
│   ├── package-lock.json
│   ├── package.json
│   ├── pytest.ini
│   ├── remove_bom.py
│   ├── reports/
│   │   └── services_discovery_summary.txt
│   ├── requirements/
│   │   ├── base.in
│   │   ├── base.txt
│   │   ├── dev.in
│   │   ├── development.txt
│   │   └── prod.in
│   ├── requirements-core.txt
│   ├── requirements-dev.txt
│   ├── requirements-observability.txt
│   ├── requirements_core.txt
│   ├── requirements_prod.txt
│   ├── requirements_test.txt
│   ├── run-tests.ps1
│   ├── run_health_check.ps1
│   ├── run_service_tests.bat
│   ├── run_service_tests.ps1
│   ├── run_service_tests_simple.ps1
│   ├── run_tests.bat
│   ├── run_tests.ps1
│   ├── scripts/
│   │   ├── audit-secrets.ps1
│   │   ├── check_imports.py
│   │   ├── compile_requirements.ps1
│   │   ├── create_admin.py
│   │   ├── create_superuser.py
│   │   ├── docs/
│   │   │   └── generate_docs.py
│   │   ├── fix_all_imports.py
│   │   ├── fix_citizenship_routes.py
│   │   ├── fix_imports.py
│   │   ├── generate_services_map.py
│   │   ├── generate_test_token.py
│   │   ├── main.py
│   │   ├── migrations/
│   │   │   ├── 001_initial_auth_schema.py
│   │   │   └── __init__.py
│   │   ├── module_health_dashboard.py
│   │   ├── requirements-db.txt
│   │   ├── run_tests.ps1
│   │   ├── run_tests.sh
│   │   ├── run_tests_with_coverage.ps1
│   │   ├── run_tests_with_coverage.sh
│   │   ├── setup_database.py
│   │   ├── setup_dev.ps1
│   │   ├── sila_cli.py
│   │   ├── start.ps1
│   │   ├── test_all_services.py
│   │   ├── test_citizenship_endpoints.py
│   │   ├── test_db_connection.py
│   │   ├── test_endpoints.py
│   │   ├── test_observability.py
│   │   ├── test_protocol_flow.py
│   │   ├── tree_modules.py
│   │   └── update_base_imports.py
│   ├── services_test_report.json
│   ├── setup_prisma_backend.ps1
│   ├── static/
│   │   └── pdfs/
│   │       ├── certificado_judicial_19.pdf
│   │       └── certificado_judicial_20.pdf
│   ├── test_commercial_fix.py
│   ├── test_commercial_schemas.py
│   ├── test_commercial_schemas_fixed.py
│   ├── test_commercial_simple.py
│   ├── test_db_connection.py
│   ├── test_login.json
│   ├── test_module_fixes.py
│   ├── test_routes.py
│   ├── test_script.ps1
│   ├── test_venv/
│   │   ├── bin/
│   │   │   ├── activate.csh
│   │   │   ├── activate.fish
│   │   │   ├── dotenv
│   │   │   └── httpx
│   │   └── pyvenv.cfg
│   ├── tests/
│   │   ├── .cascade_tmp
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── create_test.py
│   │   ├── modules/
│   │   │   ├── app/
│   │   │   │   ├── test_auth.py
│   │   │   │   ├── test_citizen.py
│   │   │   │   ├── test_crud.py
│   │   │   │   ├── test_endpoints.py
│   │   │   │   ├── test_protected.py
│   │   │   │   ├── test_schemas.py
│   │   │   │   └── test_services.py
│   │   │   ├── appointments/
│   │   │   │   └── __init__.py
│   │   │   ├── citizenship/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── conftest.py
│   │   │   │   ├── e2e_test.py
│   │   │   │   ├── measure_coverage.py
│   │   │   │   ├── run_e2e_tests.py
│   │   │   │   ├── run_error_tests.py
│   │   │   │   ├── run_integration_tests.py
│   │   │   │   ├── run_permission_tests_directly.py
│   │   │   │   ├── test_citizenship_endpoints.py
│   │   │   │   ├── test_crud.py
│   │   │   │   ├── test_error_scenarios.py
│   │   │   │   ├── test_feedback_endpoints.py
│   │   │   │   ├── test_feedback_service.py
│   │   │   │   ├── test_integration_endpoints.py
│   │   │   │   ├── test_permissions.py
│   │   │   │   ├── test_permissions_isolated.py
│   │   │   │   ├── test_schemas.py
│   │   │   │   └── test_services.py
│   │   │   ├── commercial/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── conftest.py
│   │   │   │   ├── test_config.py
│   │   │   │   ├── test_endpoints.py
│   │   │   │   ├── test_isolated.py
│   │   │   │   ├── test_schemas.py
│   │   │   │   └── test_services.py
│   │   │   ├── common/
│   │   │   │   └── __init__.py
│   │   │   ├── complaints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── conftest.py
│   │   │   │   ├── test_config.py
│   │   │   │   ├── test_endpoints.py
│   │   │   │   ├── test_isolated.py
│   │   │   │   ├── test_isolated_endpoints.py
│   │   │   │   ├── test_service.py
│   │   │   │   └── TESTING_GUIDE.md
│   │   │   ├── education/
│   │   │   │   └── __init__.py
│   │   │   ├── health/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── conftest.py
│   │   │   │   ├── test_endpoints.py
│   │   │   │   ├── test_endpoints.py.bak
│   │   │   │   ├── test_schemas.py
│   │   │   │   └── test_services.py
│   │   │   ├── internal/
│   │   │   │   └── __init__.py
│   │   │   ├── justice/
│   │   │   │   └── __init__.py
│   │   │   ├── reports/
│   │   │   │   └── __init__.py
│   │   │   ├── sanitation/
│   │   │   │   └── __init__.py
│   │   │   ├── social/
│   │   │   │   └── __init__.py
│   │   │   ├── statistics/
│   │   │   │   └── __init__.py
│   │   │   └── urbanism/
│   │   │       └── __init__.py
│   │   ├── performance/
│   │   │   ├── citizenship_load_test.py
│   │   │   ├── config.py
│   │   │   ├── run_tests.ps1
│   │   │   └── run_tests.sh
│   │   ├── run_health_tests.py
│   │   ├── run_notification_tests.py
│   │   ├── run_test.py
│   │   ├── run_tests.py
│   │   ├── test_api.py
│   │   ├── test_app.py
│   │   ├── test_appointments.py
│   │   ├── test_audit.py
│   │   ├── test_auth.py
│   │   ├── test_auth_endpoints.py
│   │   ├── test_database.py
│   │   ├── test_database_connection.py
│   │   ├── test_debug.py
│   │   ├── test_health.py
│   │   ├── test_health_crud.py
│   │   ├── test_health_endpoints.py
│   │   ├── test_health_minimal.py
│   │   ├── test_minimal.py
│   │   ├── test_minimal_math.py
│   │   ├── test_minimal_notifications.py
│   │   ├── test_notification_service_direct.py
│   │   ├── test_notification_service_mocked.py
│   │   ├── test_notification_service_unit.py
│   │   ├── test_notifications.py
│   │   ├── test_notifications_fixed.py
│   │   ├── test_notifications_minimal.py
│   │   ├── test_notifications_simple.py
│   │   ├── test_notifications_standalone.py
│   │   ├── test_password_reset.py
│   │   ├── test_password_reset_flow.py
│   │   ├── test_permissions.py
│   │   ├── test_refresh_tokens.py
│   │   ├── test_regras_negocio.py
│   │   ├── test_settings.py
│   │   ├── test_simple.py
│   │   ├── test_user_registration.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       └── utils.py
│   ├── validate_structure.py
│   ├── verify_core_fixes.py
│   ├── verify_environment.py
│   └── verify_schema_fixes.py
├── backup/
│   └── core-20250828-140054/
│       └── core/
│           ├── __init__.py
│           ├── application.py
│           ├── approval_decorator.py
│           ├── auth.py
│           ├── auth_utils.py
│           ├── cache.py
│           ├── config/
│           │   ├── __init__.py
│           │   └── settings.py
│           ├── config.py
│           ├── db/
│           │   └── __init__.py
│           ├── deps.py
│           ├── enhanced_auth.py
│           ├── exceptions.py
│           ├── form_generator.py
│           ├── formatters.py
│           ├── i18n.py
│           ├── identity/
│           │   ├── __init__.py
│           │   ├── models.py
│           │   ├── schemas.py
│           │   └── services.py
│           ├── location/
│           │   ├── __init__.py
│           │   ├── models.py
│           │   ├── schemas.py
│           │   └── services.py
│           ├── logging.py
│           ├── logging_config.py
│           ├── metrics.py
│           ├── middleware/
│           │   └── __init__.py
│           ├── middleware.py
│           ├── notificador.py
│           ├── notification/
│           │   └── __init__.py
│           ├── observability_middleware.py
│           ├── payment/
│           │   ├── __init__.py
│           │   ├── models.py
│           │   ├── providers.py
│           │   ├── schemas.py
│           │   └── services.py
│           ├── permissions.py
│           ├── prometheus_metrics.py
│           ├── regra_negocio.py
│           ├── regras_negocio.py
│           ├── responses.py
│           ├── scheduler.py
│           ├── security.py
│           ├── structured_logging.py
│           ├── versioning.py
│           └── workflow.py
├── CHANGELOG_TECNICO.md
├── check_structure.ps1
├── credential_sanitizer.py
├── data/
│   └── clientes.csv
├── dev-up.ps1
├── devops/
│   ├── monitoring/
│   │   ├── grafana/
│   │   │   └── provisioning/
│   │   │       ├── alerting/
│   │   │       │   ├── alerting.yml
│   │   │       │   ├── alertmanager.yml
│   │   │       │   └── templates/
│   │   │       │       └── slack.tmpl
│   │   │       ├── dashboards/
│   │   │       │   ├── cpf-validation-dashboard.json
│   │   │       │   └── dashboard.yml
│   │   │       └── datasources/
│   │   │           └── datasource.yml
│   │   └── prometheus/
│   │       └── prometheus.yml
│   ├── nginx/
│   │   ├── frontend.conf
│   │   └── nginx.conf
│   └── scripts/
│       ├── deploy_producao.ps1
│       ├── deploy_producao.sh
│       ├── init_db.ps1
│       └── init_db.sh
├── django_backend_inventory.csv
├── docker-compose.override.yml
├── docker-compose.production.yml
├── docker-compose.test.yml
├── Dockerfile.test
├── docs/
│   ├── ADICIONAR_NOVOS_SERVICOS.md
│   ├── api/
│   │   └── feedback-api.md
│   ├── apresentacao_executiva_sila.md
│   ├── ARQUITETURA_ATUALIZADA.md
│   ├── carta_intencao_governador.pdf
│   ├── compliance_checklist.md
│   ├── cronograma_visual_sila.md
│   ├── estado_atual_reestruturacao.md
│   ├── estrutura_arvore_projeto.txt
│   ├── EXEMPLOS_GERACAO_SERVICOS.md
│   ├── INDICE_TECNICO.md
│   ├── integration_gateway_guide.md
│   ├── manual_utilizador.pdf
│   ├── metricas_correcao.md
│   ├── monitoring/
│   │   └── cpf_metrics.md
│   ├── plano_execucao_final_sila.md
│   ├── PLANO_IMPLEMENTACAO.md
│   ├── proposta_tecnica_sila.pdf
│   ├── recomendacoes_saneamento.md
│   ├── relatorio_estado_atual_projeto.md
│   ├── roadmap_implantacao.pdf
│   ├── servicos_criados.md
│   └── tgres.txt
├── down.ps1
├── ensure_databases.sql
├── finalize_project_cleanup.bat
├── fix_init_files.py
├── fix_linting.py
├── fix_module_structure.py
├── fix_syntax_errors.py
├── frontend/
│   ├── build_frontend.ps1
│   ├── cypress/
│   │   └── e2e/
│   │       ├── cidadania.cy.js
│   │       ├── comercial.cy.js
│   │       ├── login.cy.js
│   │       ├── permissoes.cy.js
│   │       ├── relatorios.cy.js
│   │       └── sanitario.cy.js
│   ├── fix-dependencies.ps1
│   ├── index.html
│   ├── mobileapp/
│   │   ├── App.tsx
│   │   ├── package.json
│   │   └── src/
│   │       ├── components/
│   │       │   └── .cascade_tmp
│   │       ├── screens/
│   │       │   ├── CadastroMunicipe.tsx
│   │       │   ├── CarteiraDigital.tsx
│   │       │   ├── Faturar.tsx
│   │       │   ├── Historico.tsx
│   │       │   ├── LoginScreen.tsx
│   │       │   └── Reclamar.tsx
│   │       └── utils/
│   │           └── .cascade_tmp
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.js
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── accessibility/
│   │   │   │   └── AccessibilitySystem.js
│   │   │   ├── forms/
│   │   │   │   └── FormRenderer.tsx
│   │   │   ├── layout/
│   │   │   │   ├── Footer.tsx
│   │   │   │   ├── Header.tsx
│   │   │   │   └── Layout.tsx
│   │   │   ├── Menu.jsx
│   │   │   ├── ServiceHub.tsx
│   │   │   ├── services/
│   │   │   │   └── DynamicServiceForm.tsx
│   │   │   └── shared/
│   │   │       └── ErrorFallback.tsx
│   │   ├── hooks/
│   │   │   └── useServices.ts
│   │   ├── i18n.ts
│   │   ├── index.css
│   │   ├── main.tsx
│   │   └── pages/
│   │       ├── CitizenshipPage.jsx
│   │       ├── CommercialPage.jsx
│   │       ├── DashboardPage.tsx
│   │       ├── HomePage.tsx
│   │       ├── JusticePage.jsx
│   │       ├── LoginPage.tsx
│   │       ├── NotFoundPage.tsx
│   │       ├── ReportsPage.jsx
│   │       ├── SanitationPage.jsx
│   │       ├── ServiceHubPage.tsx
│   │       ├── ServicesPage.tsx
│   │       ├── StatisticsPage.jsx
│   │       └── TrainingPage.tsx
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   ├── vite.config.ts
│   └── webapp/
│       ├── BACKEND_FRONTEND_HARMONIZATION.md
│       ├── cypress/
│       │   ├── e2e/
│       │   │   ├── 1-getting-started/
│       │   │   │   └── todo.cy.js
│       │   │   ├── 2-advanced-examples/
│       │   │   │   ├── actions.cy.js
│       │   │   │   ├── aliasing.cy.js
│       │   │   │   ├── assertions.cy.js
│       │   │   │   ├── connectors.cy.js
│       │   │   │   ├── cookies.cy.js
│       │   │   │   ├── cypress_api.cy.js
│       │   │   │   ├── files.cy.js
│       │   │   │   ├── location.cy.js
│       │   │   │   ├── misc.cy.js
│       │   │   │   ├── navigation.cy.js
│       │   │   │   ├── network_requests.cy.js
│       │   │   │   ├── querying.cy.js
│       │   │   │   ├── spies_stubs_clocks.cy.js
│       │   │   │   ├── storage.cy.js
│       │   │   │   ├── traversal.cy.js
│       │   │   │   ├── utilities.cy.js
│       │   │   │   ├── viewport.cy.js
│       │   │   │   ├── waiting.cy.js
│       │   │   │   └── window.cy.js
│       │   │   ├── authstore.cy.ts
│       │   │   ├── login.cy.ts
│       │   │   └── servicos.cy.ts
│       │   ├── fixtures/
│       │   │   └── example.json
│       │   └── support/
│       │       ├── commands.js
│       │       └── e2e.js
│       ├── cypress.config.js
│       ├── Dockerfile
│       ├── fix-dependencies.ps1
│       ├── IMPLEMENTATION_STATUS.md
│       ├── index.html
│       ├── jest.config.js
│       ├── jest.setup.js
│       ├── nginx.conf
│       ├── package-lock.json
│       ├── package.json
│       ├── postcss.config.js
│       ├── public/
│       │   ├── .cascade_tmp
│       │   ├── favicon.ico
│       │   ├── manifest.json
│       │   └── sw.js
│       ├── scripts/
│       │   ├── audit-plan-consistency.mjs
│       │   ├── check-broken-imports.js
│       │   ├── check_accessibility.js
│       │   ├── fix-broken-imports.js
│       │   └── README-REORGANIZATION.md
│       ├── src/
│       │   ├── __tests__/
│       │   │   ├── Button.test.tsx
│       │   │   ├── FileInput.test.tsx
│       │   │   ├── Input.test.tsx
│       │   │   ├── LoginForm.test.tsx
│       │   │   └── RegistroMunicipeForm.test.tsx
│       │   ├── api/
│       │   │   └── axios.ts
│       │   ├── App.tsx
│       │   ├── assets/
│       │   │   └── .cascade_tmp
│       │   ├── components/
│       │   │   ├── AdminDashboard.tsx
│       │   │   ├── auth/
│       │   │   │   └── ProtectedRoute.tsx
│       │   │   ├── CitizenInfoCard.tsx
│       │   │   ├── common/
│       │   │   │   ├── LoadingSpinner.tsx
│       │   │   │   └── Logo.tsx
│       │   │   ├── Dashboard.tsx
│       │   │   ├── governance/
│       │   │   │   └── AuditLogDetails.tsx
│       │   │   ├── LanguageSelector.tsx
│       │   │   ├── layout/
│       │   │   │   ├── BasicLayout.tsx
│       │   │   │   ├── Container.tsx
│       │   │   │   ├── Footer.tsx
│       │   │   │   ├── Header.tsx
│       │   │   │   ├── index.ts
│       │   │   │   ├── PageHeader.tsx
│       │   │   │   ├── ResponsiveGrid.tsx
│       │   │   │   └── ResponsiveLayout.tsx
│       │   │   ├── mobile/
│       │   │   │   ├── PWAInstallPrompt.tsx
│       │   │   │   └── SyncStatusBar.tsx
│       │   │   ├── modules/
│       │   │   │   └── ModuleCard.tsx
│       │   │   ├── MunicipeCard.tsx
│       │   │   ├── Navbar.tsx
│       │   │   ├── navigation/
│       │   │   │   ├── Breadcrumbs.tsx
│       │   │   │   ├── MobileNavigation.tsx
│       │   │   │   └── ResponsiveNav.tsx
│       │   │   ├── registry/
│       │   │   │   └── CitizenForm.tsx
│       │   │   ├── SessionExpired.tsx
│       │   │   ├── Sidebar.tsx
│       │   │   └── ui/
│       │   │       ├── Button.tsx
│       │   │       ├── Card.tsx
│       │   │       ├── FileInput.tsx
│       │   │       ├── Form.tsx
│       │   │       ├── index.ts
│       │   │       ├── Input.tsx
│       │   │       ├── Map.stories.tsx
│       │   │       ├── Map.tsx
│       │   │       ├── Select.tsx
│       │   │       └── Tabs.tsx
│       │   ├── config/
│       │   │   └── services.json
│       │   ├── config.ts
│       │   ├── context/
│       │   │   └── AuthContext.tsx
│       │   ├── data/
│       │   │   └── modules.tsx
│       │   ├── features/
│       │   │   ├── citizenship/
│       │   │   │   ├── api/
│       │   │   │   │   ├── __tests__/
│       │   │   │   │   │   └── citizenshipApi.test.ts
│       │   │   │   │   └── citizenshipApi.ts
│       │   │   │   ├── components/
│       │   │   │   │   ├── __tests__/
│       │   │   │   │   │   └── CitizenRequestForm.test.tsx
│       │   │   │   │   └── CitizenRequestForm.tsx
│       │   │   │   └── pages/
│       │   │   │       └── CitizenRequestsPage.tsx
│       │   │   └── saude/
│       │   │       ├── api.ts
│       │   │       ├── hooks.ts
│       │   │       ├── SaudeForm.tsx
│       │   │       ├── SaudeList.tsx
│       │   │       └── SaudePage.tsx
│       │   ├── hooks/
│       │   │   ├── useAuthAxios.ts
│       │   │   ├── useCitizenData.ts
│       │   │   ├── useFeatureFlags.ts
│       │   │   ├── useLeafletGeoSearch.ts
│       │   │   ├── useMobileSync.ts
│       │   │   ├── useNotify.ts
│       │   │   └── useServiceWorker.ts
│       │   ├── i18n.ts
│       │   ├── index.css
│       │   ├── layouts/
│       │   │   └── MainLayout.tsx
│       │   ├── locales/
│       │   │   ├── en.json
│       │   │   └── pt.json
│       │   ├── main.tsx
│       │   ├── pages/
│       │   │   ├── AccaoSocial.tsx
│       │   │   ├── admin/
│       │   │   │   ├── AdminDashboard.tsx
│       │   │   │   ├── Login.tsx
│       │   │   │   ├── Reports.tsx
│       │   │   │   ├── Requests.tsx
│       │   │   │   └── Users.tsx
│       │   │   ├── CadastroAmbulante.tsx
│       │   │   ├── CadastroOcorrencia.tsx
│       │   │   ├── citizen/
│       │   │   │   └── Dashboard.tsx
│       │   │   ├── CitizenDashboard.tsx
│       │   │   ├── CitizenProfilePage.tsx
│       │   │   ├── Dashboard.tsx
│       │   │   ├── EmissaoDocumentos.tsx
│       │   │   ├── Estatisticas.tsx
│       │   │   ├── FinanceDashboard.tsx
│       │   │   ├── GovernancePanel.tsx
│       │   │   ├── HomePage.tsx
│       │   │   ├── Internos.tsx
│       │   │   ├── Licenciamento.tsx
│       │   │   ├── Login.tsx
│       │   │   ├── LoginPage.tsx
│       │   │   ├── ModulePage.tsx
│       │   │   ├── modules/
│       │   │   │   ├── CidadaniaPage.tsx
│       │   │   │   ├── citizenship/
│       │   │   │   │   ├── AtestadoPage.tsx
│       │   │   │   │   ├── DocumentosPage.tsx
│       │   │   │   │   └── RegistroPage.tsx
│       │   │   │   ├── ComercioPage.tsx
│       │   │   │   ├── EducacaoPage.tsx
│       │   │   │   ├── education/
│       │   │   │   │   ├── BoletimPage.tsx
│       │   │   │   │   ├── MatriculaPage.tsx
│       │   │   │   │   └── TransferenciaPage.tsx
│       │   │   │   ├── health/
│       │   │   │   │   ├── AgendamentoPage.tsx
│       │   │   │   │   ├── ConsultasPage.tsx
│       │   │   │   │   └── VacinasPage.tsx
│       │   │   │   ├── SaudePage.tsx
│       │   │   │   ├── urbanism/
│       │   │   │   │   ├── AlvaraFuncionamentoPage.tsx
│       │   │   │   │   ├── LicencaConstrucaoPage.tsx
│       │   │   │   │   └── ObrasPage.tsx
│       │   │   │   └── UrbanismoPage.tsx
│       │   │   ├── Reclamacoes.tsx
│       │   │   ├── RegisterPage.tsx
│       │   │   ├── RegistroMunicipe.tsx
│       │   │   ├── RegistryPage.tsx
│       │   │   ├── ServiceDetails.tsx
│       │   │   ├── Servicos.tsx
│       │   │   └── UnauthorizedPage.tsx
│       │   ├── routes/
│       │   │   ├── ProtectedRoute.tsx
│       │   │   └── RoleGuard.tsx
│       │   ├── scripts/
│       │   │   └── organize-by-domain.js
│       │   ├── services/
│       │   │   ├── api.ts
│       │   │   ├── modelUIs.tsx
│       │   │   ├── monitoring/
│       │   │   │   └── analytics.ts
│       │   │   └── ServiceView.tsx
│       │   ├── store/
│       │   │   └── auth.ts
│       │   ├── stories/
│       │   │   ├── Button.stories.tsx
│       │   │   ├── FileInput.stories.tsx
│       │   │   └── Input.stories.tsx
│       │   ├── test-utils/
│       │   │   └── mockApi.ts
│       │   ├── types/
│       │   │   └── leaflet-geosearch.d.ts
│       │   ├── utils/
│       │   │   ├── cn.ts
│       │   │   ├── console.ts
│       │   │   ├── formatters.test.ts
│       │   │   └── formatters.ts
│       │   └── validations/
│       │       ├── loginSchema.ts
│       │       └── registroMunicipeSchema.ts
│       ├── tailwind.config.js
│       ├── tsconfig.json
│       ├── tsconfig.node.json
│       └── vite.config.ts
├── generate_tree.py
├── htmlcov/
│   ├── class_index.html
│   ├── coverage_html_cb_497bf287.js
│   ├── favicon_32_cb_58284776.png
│   ├── function_index.html
│   ├── index.html
│   ├── keybd_closed_cb_ce680311.png
│   ├── status.json
│   └── style_cb_dca529e9.css
├── infra/
│   └── db/
├── init_project.ps1
├── issues_analysis_report.md
├── k8s/
│   └── sila-deployment.yaml
├── list_structure.ps1
├── log_uniformizacao_envs.txt
├── logs/
│   ├── coverage-validado.txt
│   ├── dependencies_20250818-041935.csv
│   ├── deps_dev_20250818-042313.csv
│   ├── dev/
│   │   ├── start-log-20250819-095146.md
│   │   ├── start-log-20250819-112410.md
│   │   ├── start-log-20250819-142554.md
│   │   ├── start-log-20250820-005249.md
│   │   ├── start-log-20250820-022714.md
│   │   ├── stop-log-20250819-114621.md
│   │   ├── stop-log-20250819-120527.md
│   │   └── stop-log-20250819-142127.md
│   ├── hooks_diff_2025-08-19_03-59-19.csv
│   ├── hooks_diff_2025-08-19_03-59-19.md
│   ├── pip-validado.txt
│   └── setuptools-validado.txt
├── Makefile
├── migrate_pydantic_v2.py
├── migrate_to_postgres.ps1
├── migrate_to_postgres.sh
├── models_tree.txt
├── monitoring/
│   ├── docker-compose.monitoring.yml
│   ├── grafana/
│   │   └── dashboards/
│   │       ├── sila-business.json
│   │       ├── sila-overview.json
│   │       └── sila-performance.json
│   └── prometheus/
│       ├── prometheus.yml
│       └── rules/
│           └── sila-alerts.yml
├── package-lock.json
├── package.json
├── pip.conf
├── PROJETO_LOG.md
├── relatorios/
│   └── auditoria_ignorados_20250817.txt
├── reports/
│   ├── cleanup/
│   ├── modules_tree_report.txt
│   └── setup/
│       └── sqlalchemy-models-rebuild.log
├── requirements-test.txt
├── run-tests-direct.ps1
├── run-tests-simple.bat
├── run-tests-simple.ps1
├── run-tests.bat
├── run-tests.ps1
├── run_check.bat
├── run_init.bat
├── sanear_projeto.bat
├── sanear_projeto.ps1
├── scripts/
│   ├── add_new_service.py
│   ├── analyze-project-structure.ps1
│   ├── analyze_and_migrate.ps1
│   ├── analyze_migration.py
│   ├── analyze_models.ps1
│   ├── analyze_project.ps1
│   ├── analyze_services.ps1
│   ├── api_analyzer.py
│   ├── api_endpoints.md
│   ├── audit-project.ps1
│   ├── audit_modules.ps1
│   ├── audit_modules.sh
│   ├── audit_new/
│   │   ├── check_credentials.py
│   │   └── validate_env.py
│   ├── audit_saude_refs.py
│   ├── auditar-log-padronizacao.ps1
│   ├── auditar_hooks.sh
│   ├── backend/
│   ├── batch_generate_services.py
│   ├── batch_update.py
│   ├── check-frontend-sync.py
│   ├── check-models.ps1
│   ├── check_and_generate_modules.py
│   ├── check_backend_modules.ps1
│   ├── check_backend_modules.sh
│   ├── check_backend_tests.ps1
│   ├── check_backend_tests.sh
│   ├── check_backslashes.ps1
│   ├── check_backslashes.sh
│   ├── check_binary_packages.py
│   ├── check_credentials.py
│   ├── check_db_connection.py
│   ├── check_env.ps1
│   ├── check_frontend_pages.ps1
│   ├── check_frontend_pages.sh
│   ├── check_frontend_services.ps1
│   ├── check_frontend_services.sh
│   ├── check_home_dir.ps1
│   ├── check_home_dir.sh
│   ├── check_module_integrity.py
│   ├── ci/
│   │   ├── run_tests.py
│   │   └── validate_py_syntax.py
│   ├── clean-temp.ps1
│   ├── clean_python_cache.ps1
│   ├── cleanup.ps1
│   ├── cleanup_obsolete.sh
│   ├── cleanup_obsolete_files.ps1
│   ├── convert_shell_to_powershell.ps1
│   ├── coverage_report.md
│   ├── create-service.py
│   ├── create_admin.py
│   ├── create_modules.py
│   ├── create_service.py
│   ├── create_training_module.py
│   ├── db-utils.ps1
│   ├── db_new/
│   │   ├── check_db_connection.py
│   │   └── setup_database.py
│   ├── deploy_backend.ps1
│   ├── deploy_backend.sh
│   ├── DEPLOYMENT.md
│   ├── detect_corrupted_scripts.py
│   ├── dev/
│   │   ├── create_superuser.py
│   │   └── setup_dev.py
│   ├── docs/
│   │   ├── LICENSE.md
│   │   ├── README-module-validation.md
│   │   ├── VALIDATION.md
│   │   └── VALIDATION_CHECKLIST.md
│   ├── enable_observability.py
│   ├── env.audit.md
│   ├── env_multi_preenchimento_20250818_120345.md
│   ├── env_multi_preenchimento_20250818_120407.md
│   ├── env_multi_preenchimento_20250818_120705.md
│   ├── env_multi_preenchimento_20250818_120730.md
│   ├── env_preenchimento_20250818_115728.md
│   ├── env_preenchimento_20250818_115806.md
│   ├── env_uniformizacao_log_20250819_025246.txt
│   ├── env_uniformizacao_log_20250819_025258.txt
│   ├── env_uniformizacao_log_20250820_143453.txt
│   ├── env_uniformizacao_log_20250820_143517.txt
│   ├── env_validacao_20250818_113218.md
│   ├── fix-corrupted-content.py
│   ├── fix-corrupted-filenames.ps1
│   ├── fix-imports.ps1
│   ├── fix-migration-order-simple.ps1
│   ├── fix-migration-order.ps1
│   ├── fix-notification-files.py
│   ├── fix-project.ps1
│   ├── fix-sqlalchemy-refs.py
│   ├── fix-syntax-errors.py
│   ├── fix_database_urls.ps1
│   ├── fix_encoding.py
│   ├── fix_module_structure.ps1
│   ├── fix_module_structure_fixed.ps1
│   ├── fix_syntax_errors_targeted.py
│   ├── fix_unterminated_strings.py
│   ├── fixed_encoding.ps1
│   ├── fixed_init.ps1
│   ├── fixed_init_project.ps1
│   ├── fixed_script.ps1
│   ├── frontend/
│   │   └── package.json
│   ├── generate-docs.ps1
│   ├── generate-index.ps1
│   ├── generate-migration-report.py
│   ├── generate-requirements.ps1
│   ├── generate-script-index.ps1
│   ├── generate-scripts-index.ps1
│   ├── generate_backend_models_tree.ps1
│   ├── generate_directory_backend_tree.py
│   ├── generate_models_tree.ps1
│   ├── generate_project_tree.py
│   ├── generate_service.py
│   ├── generate_test_data.py
│   ├── init_project.ps1
│   ├── init_project_simple.ps1
│   ├── list_services.ps1
│   ├── log_hook_execution.py
│   ├── main.py
│   ├── master-migration.ps1
│   ├── module_validator.py
│   ├── move_obsolete_scripts.ps1
│   ├── nuke-legacy-and-trash.ps1
│   ├── organize-python-files.ps1
│   ├── organize_backend.ps1
│   ├── padronizar_envs.py
│   ├── post-migration-audit.ps1
│   ├── pre_deploy_check.ps1
│   ├── pre_deploy_check.sh
│   ├── preencher_env_critico.py
│   ├── preencher_env_critico_multi.py
│   ├── preencher_env_critico_multi_csv.py
│   ├── quick_check.py
│   ├── rebuild-minimal-structure.ps1
│   ├── rebuild-sqlalchemy-models.ps1
│   ├── recreate-critical-files.py
│   ├── requirements_analyzer.py
│   ├── restore_notification_filenames.py
│   ├── restore_original_filenames.py
│   ├── run-tests.ps1
│   ├── run_all_validations.ps1
│   ├── run_init.bat
│   ├── run_integration_example.py
│   ├── run_tests.py
│   ├── safe-migration.ps1
│   ├── sanitize-backend-modules.ps1
│   ├── sanitize-core.ps1
│   ├── sanitize-frontend-webapp.ps1
│   ├── sanitize-frontend.ps1
│   ├── sanitize-project-root.ps1
│   ├── scripts/
│   │   ├── fix-critical-filenames.py
│   │   └── init_project_final.ps1
│   ├── set_approval_level.py
│   ├── setup_database.py
│   ├── setup_env.ps1
│   ├── setup_modules.py
│   ├── setup_project_structure.py
│   ├── setup_structure.py
│   ├── sila_migrate.py
│   ├── simple_analyze_models.ps1
│   ├── simple_init.ps1
│   ├── simple_test.ps1
│   ├── standardize-config.ps1
│   ├── sync-endpoints.ps1
│   ├── temp_script.ps1
│   ├── templates/
│   │   └── module_template/
│   ├── test-migration.ps1
│   ├── test_all_services.py
│   ├── test_coverage_reporter.py
│   ├── test_critical_routes.py
│   ├── test_execution.ps1
│   ├── test_paths.ps1
│   ├── testar_ligacoes_envs.py
│   ├── tests/
│   │   ├── generate_tests.py
│   │   ├── generate_tests_simple.py
│   │   └── test_environment.py
│   ├── True/
│   ├── uniformizar_senha_envs.py
│   ├── update_gitignore.ps1
│   ├── update_translations.py
│   ├── users_data.json
│   ├── utils_new/
│   │   ├── auto_register_modules.py
│   │   ├── diagnose_modules.py
│   │   ├── fix_imports.py
│   │   ├── production_fix.py
│   │   ├── tree_modules.py
│   │   └── validate_auth.py
│   ├── validar_env_conexao.py
│   ├── validar_env_conexao_precommit.py
│   ├── validar_env_critico.py
│   ├── validate-module-integrity.ps1
│   ├── validate-module-integrity.py
│   ├── validate-modules.ps1
│   ├── validate-py-compile.ps1
│   ├── validate_cleanup_environment.py
│   ├── validate_csv.py
│   ├── validate_implementation.py
│   ├── validate_no_sqlite.ps1
│   ├── validate_no_sqlite.sh
│   ├── validate_py_compile.py
│   ├── validate_py_syntax.py
│   └── version_service.py
├── setup.py
├── setup_env.ps1
├── setup_project.ps1
├── setup_sila_structure.ps1
├── sila_150_services.csv
├── start-project.ps1
├── STRATEGIC_EVOLUTION_COMPLETE.md
├── temp_pytest.ini
├── test-simple.ps1
├── test.ps1
├── test_drop_migration.py
├── test_drop_migration.py.bak
├── test_migration.py
├── teste_servicos.csv
├── tests/
│   ├── conftest.py
│   ├── factories/
│   │   ├── __init__.py
│   │   ├── base_factory.py
│   │   ├── citizen_factory.py
│   │   ├── license_factory.py
│   │   ├── service_factory.py
│   │   └── user_factory.py
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_citizens.py
│   │   ├── test_services.py
│   │   └── test_users.py
│   ├── modules/
│   │   ├── appointments/
│   │   │   └── test_appointments.py
│   │   ├── citizenship/
│   │   │   ├── test_citizenship.py
│   │   │   └── test_endpoints.py
│   │   ├── commercial/
│   │   │   └── test_endpoints.py
│   │   ├── education/
│   │   │   └── test_education.py
│   │   ├── health/
│   │   │   └── test_health.py
│   │   ├── internal/
│   │   │   └── test_internal.py
│   │   ├── justice/
│   │   │   └── test_justice.py
│   │   ├── reports/
│   │   │   ├── test_endpoints.py
│   │   │   └── test_reports.py
│   │   ├── sanitation/
│   │   │   └── test_endpoints.py
│   │   ├── social/
│   │   │   └── test_social.py
│   │   └── statistics/
│   │       └── test_endpoints.py
│   ├── test_config.py
│   ├── test_directory_structure.py
│   ├── test_health.py
│   └── test_utils/
│       ├── __init__.py
│       └── test_db.py
├── True/
├── truman_try.txt
├── update_models.py
├── validation_report.json
└── validation_report.md
```
