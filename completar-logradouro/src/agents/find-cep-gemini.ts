import { Injectable } from "@nestjs/common";
import OpenAI from "openai";
import { CepInformation } from "./cep-information";

const apiKey = process.env.GOOGLE_API_KEY ?? "";

@Injectable()
export class FindCEPGemini {
    private readonly client: OpenAI;

    constructor() {
        const baseURL = "https://generativelanguage.googleapis.com/v1beta/openai/";
        
        this.client = new OpenAI({
            apiKey,
            baseURL
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
            model: "gemini-2.5-flash",
            messages: [
                {
                    role: "user",
                    content: prompt,
                },
            ]
        });
        const output = JSON.parse(completion.choices[0].message.content || "{}") as CepInformation;
        return output;
    }
    
}