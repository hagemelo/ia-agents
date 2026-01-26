import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { FindCEPOpenAI } from './agents/find-cep-openai';

@Module({
  imports: [],
  controllers: [AppController],
  providers: [AppService, FindCEPOpenAI],
})
export class AppModule {}
