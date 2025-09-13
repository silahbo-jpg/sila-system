import React, { useState, useCallback } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { api } from "../api/axios";
import { registroMunicipeSchema, RegistroMunicipeFormData } from "../validations/registroMunicipeSchema";
import { Form, Input, Button, FileInput } from "../components/ui";

export default function RegistroMunicipe() {
  const [fotoPreview, setFotoPreview] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const methods = useForm<RegistroMunicipeFormData>({
    resolver: zodResolver(registroMunicipeSchema),
    mode: 'onChange', // Validação em tempo real
  });

  const { register, handleSubmit, formState: { errors }, watch, setValue, trigger } = methods;

  // Observa mudanças nos campos de arquivo para atualizar os previews
  const fotoFileList = watch("foto");

  // Atualiza o preview da foto quando o arquivo mudar
  React.useEffect(() => {
    if (fotoFileList?.length > 0) {
      const file = fotoFileList[0];
      setFotoPreview(URL.createObjectURL(file));
    } else {
      setFotoPreview(null);
    }
  }, [fotoFileList]);

  const onSubmit = async (data: RegistroMunicipeFormData) => {
    try {
      setIsSubmitting(true);
      const formData = new FormData();
      
      // Adiciona os campos ao FormData
      Object.entries(data).forEach(([key, value]) => {
        if (value instanceof FileList && value.length > 0) {
          formData.append(key, value[0]);
        } else if (value !== undefined && value !== null) {
          formData.append(key, value);
        }
      });

      await api.post("/municipe", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      alert("Munícipe registrado com sucesso!");
      // Resetar o formulário após o envio bem-sucedido
      (document.getElementById('registroForm') as HTMLFormElement)?.reset();
      setFotoPreview(null);
    } catch (error) {
      console.error("Erro ao registrar munícipe:", error);
      alert("Ocorreu um erro ao registrar o munícipe. Por favor, tente novamente.");
    } finally {
      setIsSubmitting(false);
    }
  };

  // Função para formatar o número do BI enquanto o usuário digita
  const formatarBI = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    let value = e.target.value.replace(/[^a-zA-Z0-9]/g, '').toUpperCase();
    if (value.length > 0) {
      // Formato: 999999999LA042
      value = value.replace(/^(\d{0,9})([A-Za-z]{0,2})(\d{0,3})/, (match, p1, p2, p3) => {
        return p1 + p2 + p3;
      });
    }
    setValue('numero_bi', value);
    trigger('numero_bi'); // Dispara a validação
  }, [setValue, trigger]);

  // Renderiza o preview da foto
  const renderFotoPreview = useCallback(() => {
    if (!fotoPreview) return null;
    
    return (
      <div className="mt-2">
        <p className="text-sm font-medium text-gray-700 mb-1">Pré-visualização:</p>
        <img 
          src={fotoPreview} 
          alt="Preview da Foto" 
          className="w-32 h-32 object-cover rounded-md border border-gray-200" 
        />
      </div>
    );
  }, [fotoPreview]);

  return (
    <div className="p-6 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-gray-800">Registro de Munícipe</h1>
      
      <Form methods={methods} onSubmit={onSubmit}>
        {/* Campo Nome */}
        <Input
          label="Nome Completo"
          id="nome"
          type="text"
          placeholder="Digite o nome completo"
          error={errors.nome}
          register={register('nome')}
          required
        />

        {/* Campo Número do BI */}
        <div>
          <Input
            label="Número do BI"
            id="numero_bi"
            type="text"
            placeholder="Ex: 123456789LA042"
            error={errors.numero_bi}
            register={register('numero_bi')}
            onChange={formatarBI}
            required
          />
          {!errors.numero_bi && (
            <p className="mt-1 text-xs text-gray-500">Formato: 9 dígitos + 2 letras + 3 dígitos</p>
          )}
        </div>

        {/* Campo Foto */}
        <FileInput
          label="Foto do Rosto"
          id="foto"
          accept="image/*"
          error={errors.foto as FieldError | undefined}
          register={register('foto')}
          preview={renderFotoPreview()}
          helperText="Formatos aceitos: JPG, PNG, etc."
        />

        {/* Campo Anexo do BI */}
        <FileInput
          label="Anexo do BI (PDF)"
          id="bi_anexo"
          accept="application/pdf"
          error={errors.bi_anexo as FieldError | undefined}
          register={register('bi_anexo')}
          helperText="Envie o arquivo digitalizado do seu BI em formato PDF"
        />

        {/* Botão de Envio */}
        <div className="pt-2">
          <Button
            type="submit"
            variant="primary"
            size="lg"
            isLoading={isSubmitting}
            fullWidth
          >
            Registrar Munícipe
          </Button>
        </div>
      </Form>
    </div>
  );
}

