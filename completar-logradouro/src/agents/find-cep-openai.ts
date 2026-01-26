import { Injectable } from "@nestjs/common";
import OpenAI from "openai";
import { CepInformation } from "./cep-information";

const apiKey = process.env.OPENAI_API_KEY ?? "";

@Injectable()
export class FindCEPOpenAI {
    private readonly client: OpenAI;

    constructor() {

        this.client = new OpenAI({
            apiKey,
        });
    }

    public async getCepInformation(cep: string): Promise<CepInformation> {

        const prompt = `
        Você é um agente de busca de informações de CEP.
        Você deve buscar as informações de um CEP e retornar as informações de forma estruturada.
        O CEP é: ${cep}.
        Retorne as informações de forma estruturada, em JSON, exemplo:
        { 
            "cep": string;
            "logradouro": string;
            "bairro": string;
            "cidade": string;
            "estado": string;
            "siglaEstado": string;
        }
        `;

        const completion = await this.client.chat.completions.create({
            model: "gpt-4o-mini",
            messages: [
                {
                    role: "user",
                    content: prompt,
                },
            ],
            response_format: {
                type: "json_schema",
                json_schema: {
                    name: "cep_information",
                    schema: {
                        type: "object",
                        properties: {
                            cep: { type: "string" },
                            logradouro: { type: "string" },
                            bairro: { type: "string" },
                            cidade: { type: "string" },
                            estado: { type: "string" },
                            siglaEstado: { type: "string" },
                        },
                        required: ["cep", "logradouro", "bairro", "cidade", "estado", "siglaEstado"],
                        additionalProperties: false,
                    },
                },
            },
        });
        const output = JSON.parse(completion.choices[0].message.content || "{}") as CepInformation;
        return output;
    }
    
}