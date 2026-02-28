import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { FindCEPOpenAI } from './agents/find-cep-openai';
import { FindCEPGemini } from './agents/find-cep-gemini';

@Module({
  imports: [],
  controllers: [AppController],
  providers: [AppService, FindCEPOpenAI, FindCEPGemini],
})
export class AppModule {}
